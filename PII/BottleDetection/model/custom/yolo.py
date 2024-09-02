import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
import torchvision
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from PIL import Image

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_dir = os.path.join(root_dir, 'images')
        self.label_dir = os.path.join(root_dir, 'labels')
        self.image_names = os.listdir(self.image_dir)

    def __getitem__(self, idx):
        # Retrieve an image and its annotations based on index
        image_name = self.image_names[idx]
        image_path = os.path.join(self.image_dir, image_name)
        label_path = os.path.join(self.label_dir, image_name.replace('.jpg', '.txt'))
        
        # Load the image
        image = Image.open(image_path).convert("RGB")
        
        # Load the annotations
        with open(label_path, 'r') as f:
            # Process your label file here and store the annotations in an appropriate data structure
            annotations = f.read().strip()
        
        # Apply transformations if provided
        if self.transform is not None:
            image = self.transform(image)
        
        return image, annotations

    def __len__(self):
        # Return the total number of samples in the dataset
        return len(self.image_names)

# Define the model architecture
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
backbone = model.backbone
in_channels = backbone.out_channels

# Modify the backbone to include the out_channels attribute
backbone.out_channels = in_channels

# Modify the model to fit your custom dataset
num_classes = 2  # Assuming you have two classes: bottle and background
model.roi_heads.box_predictor = nn.Linear(in_channels, num_classes)

# Define the data transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    # Add any additional transformations you require
])

# Load the dataset
train_dataset = CustomDataset('C:/Users/ADMIN/Documents/myfolder/GitHub/PII-Robot/BottleDetection/training/dataset/train', transform=transform)
test_dataset = CustomDataset('C:/Users/ADMIN/Documents/myfolder/GitHub/PII-Robot/BottleDetection/training/dataset/validation', transform=transform)

# Define the data loaders
train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True, num_workers=4)
test_dataloader = DataLoader(test_dataset, batch_size=4, shuffle=False, num_workers=4)

# Define the optimizer and loss function
params = [p for p in model.parameters() if p.requires_grad]
optimizer = optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
criterion = nn.CrossEntropyLoss()

# Train the model
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)
model.train()

num_epochs = 10
for epoch in range(num_epochs):
    for images, targets in train_dataloader:
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        
        optimizer.zero_grad()
        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        losses.backward()
        optimizer.step()

# Save the trained model
torch.save(model.state_dict(), 'trained_model.pt')