# import os
# import shutil

# current_path = os.getcwd()
# folder_path = os.path.join(current_path,'BottleDetection/training/bottle-dataset/train')  # Replace with the path to your folder


# image_folder = os.path.join(current_path,'BottleDetection/training/bottle-dataset/images')
# annotation_folder = os.path.join(current_path,'BottleDetection/training/bottle-dataset/annotations')

# os.makedirs(image_folder, exist_ok=True)
# os.makedirs(annotation_folder, exist_ok=True)

# for filename in os.listdir(folder_path):
#     if filename.endswith(".jpg"):
#         image_path = os.path.join(folder_path, filename)
#         shutil.move(image_path, image_folder)
#     elif filename.endswith(".xml"):
#         annotation_path = os.path.join(folder_path, filename)
#         shutil.move(annotation_path, annotation_folder)

import os
import xml.etree.ElementTree as ET

# Path to the folder containing XML files
folder_path = os.path.join(os.getcwd(), "BottleDetection/training/bottle-dataset/annotations")

# Set to store unique names
unique_names = set()

# Iterate over each XML file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".xml"):
        file_path = os.path.join(folder_path, file_name)

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find all <name> tags and extract the name
        for name_tag in root.findall(".//name"):
            name = name_tag.text
            unique_names.add(name)

# Print the unique names
for name in unique_names:
    print(name)