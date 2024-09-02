import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

import os
from PIL import Image
import xml.etree.ElementTree as ET

current_path = os.getcwd()

# Set device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define your custom dataset
class CustomDataset(Dataset):
    def __init__(self, image_folder, annotation_folder, transform=None):
        self.image_folder = image_folder
        self.annotation_folder = annotation_folder
        self.transform = transform

        self.image_files = os.listdir(image_folder)
        self.annotation_files = os.listdir(annotation_folder)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = os.path.join(self.image_folder, self.image_files[idx])
        annotation_path = os.path.join(self.annotation_folder, self.annotation_files[idx])

        # Load image
        image = Image.open(image_path).convert("RGB")

        # Load annotation
        annotation = self.parse_annotation(annotation_path)

        # Apply transformations if specified
        if self.transform is not None:
            image = self.transform(image)

        return image, annotation

    def parse_annotation(self, annotation_path):
        tree = ET.parse(annotation_path)
        root = tree.getroot()

        annotation = []

        for obj in root.findall('object'):
            name = obj.find('name').text
            if name in ['bottle cap', 'open bottle']:
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)

                annotation.append([xmin, ymin, xmax, ymax])

        return torch.tensor(annotation)

# Define your custom model architecture
class CustomModel(nn.Module):
    def __init__(self, num_classes):
        super(CustomModel, self).__init__()

        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.fc = nn.Linear(32 * 8 * 8, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)  # Reshape x to (16, 100352)
        x = self.fc(x)  # Perform matrix multiplication
        return x

# Set hyperparameters
image_folder = os.path.join(current_path, "BottleDetection/training/bottle-dataset/images")
annotation_folder = os.path.join(current_path, "BottleDetection/training/bottle-dataset/annotations")
num_classes = 1
batch_size = 16
learning_rate = 0.001
num_epochs = 10

# Define transformations for data augmentation
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize image to a fixed size
    transforms.ToTensor(),  # Convert image to tensor
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize image tensor
])

# Create an instance of the custom dataset
dataset = CustomDataset(image_folder=image_folder, annotation_folder=annotation_folder, transform=transform)

# Split the dataset into train and validation sets
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

# Create data loaders for train and validation sets
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# Create an instance of the custom model
model = CustomModel(num_classes).to(device)

# Define the loss function and optimizer
criterion = nn.SmoothL1Loss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for images, annotations in train_loader:
        images = images.to(device)
        annotations = annotations.to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, annotations)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    # Calculate average training loss
    avg_loss = running_loss / len(train_loader)

    # Print training metrics for each epoch
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}')

# Save the trained model
torch.save(model.state_dict(), 'custom_model.pth')