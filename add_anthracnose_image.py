"""
Helper script to add anthracnose images to the dataset
"""

import os
import shutil
from pathlib import Path

def add_anthracnose_image(image_path, dataset_dir="data/PlantVillage"):
    """
    Add an anthracnose image to the dataset
    
    Args:
        image_path (str): Path to the anthracnose image file
        dataset_dir (str): Path to the dataset directory
    """
    anthracnose_dir = os.path.join(dataset_dir, "Anthracnose")
    os.makedirs(anthracnose_dir, exist_ok=True)
    
    # Get the filename
    filename = os.path.basename(image_path)
    
    # Count existing images to create unique name
    existing_images = [f for f in os.listdir(anthracnose_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    num_existing = len(existing_images)
    
    # Create new filename
    name, ext = os.path.splitext(filename)
    new_filename = f"sample_{num_existing:03d}{ext}"
    dest_path = os.path.join(anthracnose_dir, new_filename)
    
    # Copy the image
    shutil.copy2(image_path, dest_path)
    print(f"✅ Added image to: {dest_path}")
    print(f"📊 Total anthracnose images: {num_existing + 1}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python add_anthracnose_image.py <path_to_image>")
        print("Example: python add_anthracnose_image.py my_anthracnose_leaf.jpg")
    else:
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            add_anthracnose_image(image_path)
        else:
            print(f"❌ Error: Image file not found: {image_path}")

