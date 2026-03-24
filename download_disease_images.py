"""
Script to help download plant disease images from public sources
Note: This script provides guidance and can download from specific public APIs
For Google Images, you'll need to manually download or use a browser extension
"""

import os
import requests
from pathlib import Path
import time

# Disease folders that need images
DISEASE_FOLDERS = {
    'Anthracnose': 'anthracnose plant disease',
    'Apple___Black_rot': 'apple black rot disease',
    'Apple___Cedar_apple_rust': 'apple cedar rust disease',
    'Corn___Common_rust': 'corn common rust disease',
    'Corn___Cercospora_leaf_spot': 'corn cercospora leaf spot',
    'Corn___Northern_Leaf_Blight': 'corn northern leaf blight',
    'Corn___healthy': 'healthy corn plant',
    'Grape___Black_rot': 'grape black rot disease',
    'Grape___Esca': 'grape esca disease',
    'Grape___Leaf_blight': 'grape leaf blight disease',
    'Grape___healthy': 'healthy grape plant',
    'Pepper_bell___Bacterial_spot': 'pepper bacterial spot disease',
    'Pepper_bell___healthy': 'healthy bell pepper plant',
    'Cherry_Powdery_mildew': 'cherry powdery mildew disease',
    'Cherry_healthy': 'healthy cherry plant',
    'Strawberry___Leaf_scorch': 'strawberry leaf scorch disease',
    'Strawberry___healthy': 'healthy strawberry plant',
    'Peach___Bacterial_spot': 'peach bacterial spot disease',
    'Peach___healthy': 'healthy peach plant',
    'Blueberry___healthy': 'healthy blueberry plant',
    'Orange___Haunglongbing': 'citrus greening disease',
    'Soybean___healthy': 'healthy soybean plant',
    'Raspberry___healthy': 'healthy raspberry plant',
    'Squash___Powdery_mildew': 'squash powdery mildew disease',
    'Squash___healthy': 'healthy squash plant',
    'Tomato___Bacterial_spot': 'tomato bacterial spot disease',
    'Tomato___Late_blight': 'tomato late blight disease',
    'Tomato___Leaf_Mold': 'tomato leaf mold disease',
    'Tomato___Septoria_leaf_spot': 'tomato septoria leaf spot disease',
    'Tomato___Spider_mites': 'tomato spider mites damage',
    'Tomato___Target_Spot': 'tomato target spot disease',
    'Tomato___Tomato_mosaic_virus': 'tomato mosaic virus disease',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'tomato yellow leaf curl virus',
    'Potato___Early_blight': 'potato early blight disease',
}

def create_download_instructions():
    """Create instructions file for downloading images"""
    instructions = """
# How to Download Plant Disease Images

## Method 1: Manual Download (Recommended)
1. Go to Google Images: https://images.google.com
2. Search for each disease (see search terms below)
3. Filter by "Usage rights" -> "Labeled for reuse"
4. Download 20-30 images per disease
5. Save them to the corresponding folder in data/PlantVillage/

## Method 2: Use PlantVillage Dataset (Best Quality)
The PlantVillage dataset is the best source for plant disease images:
- Website: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- Or: https://github.com/spMohanty/PlantVillage-Dataset
- Contains thousands of labeled plant disease images
- Free to use for research/educational purposes

## Method 3: Use Browser Extension
- Install "Image Downloader" extension for Chrome/Firefox
- Search Google Images with filters
- Bulk download images
- Organize into folders

## Search Terms for Each Disease:
"""
    
    for folder, search_term in DISEASE_FOLDERS.items():
        instructions += f"\n- {folder}: Search '{search_term}'"
    
    instructions += """

## Image Requirements:
- Format: JPG, JPEG, or PNG
- Size: At least 224x224 pixels (larger is better)
- Quality: Clear, focused images showing disease symptoms
- Quantity: 20-50 images per disease for good accuracy

## After Downloading:
1. Place images in: data/PlantVillage/[Disease_Name]/
2. Retrain model: python train_model.py --data_dir "data/PlantVillage" --epochs 50
"""
    
    with open('DOWNLOAD_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Created DOWNLOAD_INSTRUCTIONS.md with detailed guidance")

def create_batch_download_script():
    """Create a PowerShell script to help organize downloads"""
    script = """# PowerShell script to help organize downloaded images
# Run this after downloading images to organize them

$baseDir = "data\\PlantVillage"

# Function to move images to correct folders
function Move-ImagesToFolder {
    param(
        [string]$SourceFolder,
        [string]$DiseaseFolder,
        [string]$Pattern = "*.jpg,*.jpeg,*.png"
    )
    
    $targetPath = Join-Path $baseDir $DiseaseFolder
    if (Test-Path $targetPath) {
        $images = Get-ChildItem -Path $SourceFolder -Include $Pattern -Recurse
        foreach ($img in $images) {
            $dest = Join-Path $targetPath $img.Name
            Copy-Item $img.FullName $dest -Force
            Write-Host "Copied: $($img.Name) to $DiseaseFolder"
        }
    }
}

Write-Host "Image Organization Script"
Write-Host "Place your downloaded images in a folder, then update the script"
"""
    
    with open('organize_images.ps1', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("✅ Created organize_images.ps1 helper script")

def check_folder_status():
    """Check which folders have images and which are empty"""
    base_dir = Path("data/PlantVillage")
    status = {}
    
    for folder_name in DISEASE_FOLDERS.keys():
        folder_path = base_dir / folder_name
        if folder_path.exists():
            images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.jpeg")) + list(folder_path.glob("*.png"))
            status[folder_name] = len(images)
        else:
            status[folder_name] = 0
    
    print("\n📊 Folder Status:")
    print("=" * 50)
    empty = []
    has_images = []
    
    for folder, count in sorted(status.items()):
        if count == 0:
            empty.append(folder)
            print(f"❌ {folder}: {count} images")
        else:
            has_images.append(folder)
            print(f"✅ {folder}: {count} images")
    
    print("\n" + "=" * 50)
    print(f"Empty folders: {len(empty)}")
    print(f"Folders with images: {len(has_images)}")
    
    return status

if __name__ == "__main__":
    print("🌱 Plant Disease Image Download Helper")
    print("=" * 50)
    
    # Create instructions
    create_download_instructions()
    create_batch_download_script()
    
    # Check current status
    check_folder_status()
    
    print("\n📝 Next Steps:")
    print("1. Read DOWNLOAD_INSTRUCTIONS.md for detailed guidance")
    print("2. Download images using one of the methods described")
    print("3. Place images in the corresponding folders")
    print("4. Run this script again to check status")
    print("5. Retrain model after adding images")

