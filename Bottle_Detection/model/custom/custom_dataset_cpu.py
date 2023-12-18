import torch
import torch.nn as nn
from torch.utils.data import Dataset
from PIL import Image
import os
import xml.etree.ElementTree as ET
import torch.optim as optim
from torchvision import transforms

current_path = os.getcwd()
image_folder = os.path.join(current_path, 'BottleDetection/training/bottle-dataset/images')
annotation_folder = os.path.join(current_path, 'BottleDetection/training/bottle-dataset/annotations')

num_classes = 1
batch_size = 16
learning_rate = 0.001
num_epochs = 10

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
            if name == 'open bottle':  # Adjust the class name as per your dataset
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)

                annotation.append([xmin, ymin, xmax, ymax])

        return torch.tensor(annotation)
    
class CustomModel(nn.Module):
    def __init__(self, num_classes):
        super(CustomModel, self).__init__()

        # Define your custom model architecture
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.fc = nn.Linear(32 * 8 * 8, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
            
def create_model(num_classes):
    return CustomModel(num_classes)

dataset = CustomDataset(image_folder=image_folder, annotation_folder=annotation_folder)
model = create_model(num_classes)

def custom_collate_fn(batch):
    images = []
    annotations = []
    for image, annotation in batch:
        images.append(transforms.ToTensor()(image))
        annotations.append(annotation)

    return torch.stack(images), annotations

# Update the train_loader with the custom_collate_fn
train_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=custom_collate_fn)
val_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    model.train()
    for images, labels in train_loader:
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            # Perform evaluation or calculate validation metrics

    # Print training and validation metrics for each epoch
    print(f'Epoch: {epoch+1}/{num_epochs}, Loss: {loss.item()}, Validation Metrics: ...')

torch.save(model.state_dict(), 'custom_model.pth')