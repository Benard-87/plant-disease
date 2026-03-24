"""
Automated image downloader for plant disease images
Uses Bing Image Search API (free tier available) or manual download assistance
"""

import os
import requests
from pathlib import Path
import json
import time

# Disease search terms
DISEASE_SEARCH_TERMS = {
    'Anthracnose': ['anthracnose plant disease', 'anthracnose leaf spot'],
    'Apple___Black_rot': ['apple black rot disease', 'apple black rot symptoms'],
    'Apple___Cedar_apple_rust': ['apple cedar rust', 'cedar apple rust disease'],
    'Corn___Common_rust': ['corn rust disease', 'corn common rust'],
    'Corn___Cercospora_leaf_spot': ['corn cercospora', 'corn gray leaf spot'],
    'Corn___Northern_Leaf_Blight': ['corn northern leaf blight', 'corn leaf blight'],
    'Corn___healthy': ['healthy corn plant', 'healthy corn leaves'],
    'Grape___Black_rot': ['grape black rot disease', 'grape black rot symptoms'],
    'Grape___Esca': ['grape esca disease', 'grape esca symptoms'],
    'Grape___Leaf_blight': ['grape leaf blight', 'grape leaf disease'],
    'Grape___healthy': ['healthy grape plant', 'healthy grape leaves'],
    'Pepper_bell___Bacterial_spot': ['pepper bacterial spot', 'bell pepper disease'],
    'Pepper_bell___healthy': ['healthy bell pepper', 'healthy pepper plant'],
    'Cherry_Powdery_mildew': ['cherry powdery mildew', 'cherry tree disease'],
    'Cherry_healthy': ['healthy cherry tree', 'healthy cherry leaves'],
    'Strawberry___Leaf_scorch': ['strawberry leaf scorch', 'strawberry disease'],
    'Strawberry___healthy': ['healthy strawberry plant', 'healthy strawberry'],
    'Peach___Bacterial_spot': ['peach bacterial spot', 'peach tree disease'],
    'Peach___healthy': ['healthy peach tree', 'healthy peach leaves'],
    'Blueberry___healthy': ['healthy blueberry plant', 'healthy blueberry'],
    'Orange___Haunglongbing': ['citrus greening disease', 'huanglongbing citrus'],
    'Soybean___healthy': ['healthy soybean plant', 'healthy soybean'],
    'Raspberry___healthy': ['healthy raspberry plant', 'healthy raspberry'],
    'Squash___Powdery_mildew': ['squash powdery mildew', 'squash disease'],
    'Squash___healthy': ['healthy squash plant', 'healthy squash'],
    'Tomato___Bacterial_spot': ['tomato bacterial spot', 'tomato bacterial disease'],
    'Tomato___Late_blight': ['tomato late blight', 'tomato blight disease'],
    'Tomato___Leaf_Mold': ['tomato leaf mold', 'tomato mold disease'],
    'Tomato___Septoria_leaf_spot': ['tomato septoria', 'septoria leaf spot'],
    'Tomato___Spider_mites': ['tomato spider mites', 'tomato mite damage'],
    'Tomato___Target_Spot': ['tomato target spot', 'target spot disease'],
    'Tomato___Tomato_mosaic_virus': ['tomato mosaic virus', 'tomato virus disease'],
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': ['tomato yellow leaf curl', 'TYLCV disease'],
    'Potato___Early_blight': ['potato early blight', 'potato blight disease'],
}

def create_google_images_urls():
    """Create Google Images search URLs for each disease"""
    base_url = "https://www.google.com/search?tbm=isch&q="
    
    urls_file = "google_images_urls.txt"
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write("# Google Images Search URLs for Plant Diseases\n")
        f.write("# Copy these URLs and open in browser to download images\n")
        f.write("# Remember to filter by 'Labeled for reuse'\n\n")
        
        for folder, search_terms in DISEASE_SEARCH_TERMS.items():
            f.write(f"\n# {folder}\n")
            for term in search_terms:
                url = base_url + term.replace(' ', '+')
                f.write(f"{url}\n")
    
    print(f"✅ Created {urls_file} with Google Images search URLs")

def create_download_script():
    """Create a script to help with manual downloads"""
    script = """# PowerShell script to help organize downloaded images
# After downloading images from Google/PlantVillage, use this to organize them

$downloadsFolder = "$env:USERPROFILE\\Downloads"  # Change if your downloads are elsewhere
$targetBase = "data\\PlantVillage"

Write-Host "Image Organization Helper"
Write-Host "=" * 50

# Function to count images in a folder
function Count-Images {
    param([string]$Path)
    $images = Get-ChildItem -Path $Path -Include *.jpg,*.jpeg,*.png -ErrorAction SilentlyContinue
    return $images.Count
}

# Check each disease folder
$folders = Get-ChildItem -Path $targetBase -Directory
foreach ($folder in $folders) {
    $count = Count-Images $folder.FullName
    if ($count -gt 0) {
        Write-Host "✅ $($folder.Name): $count images" -ForegroundColor Green
    } else {
        Write-Host "❌ $($folder.Name): 0 images" -ForegroundColor Red
    }
}

Write-Host "`nTo add images:"
Write-Host "1. Download images from Google Images or PlantVillage dataset"
Write-Host "2. Copy images to: $targetBase\\[Disease_Folder]\\"
Write-Host "3. Run this script again to check status"
"""
    
    with open('check_images.ps1', 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("✅ Created check_images.ps1 helper script")

def create_plantvillage_guide():
    """Create guide for using PlantVillage dataset"""
    guide = """# Using PlantVillage Dataset (RECOMMENDED)

## Why PlantVillage?
- ✅ 54,000+ high-quality images
- ✅ Already labeled and organized
- ✅ Free for research/educational use
- ✅ Professional quality
- ✅ No copyright issues

## How to Get It:

### Option 1: Kaggle (Easiest)
1. Go to: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
2. Click "Download" (requires free Kaggle account)
3. Extract the ZIP file
4. Copy images to your folders

### Option 2: GitHub
1. Go to: https://github.com/spMohanty/PlantVillage-Dataset
2. Clone or download the repository
3. Extract images
4. Copy to your folders

## Quick Copy Script:

After downloading PlantVillage dataset, use this PowerShell script:

```powershell
# Set paths
$plantVillagePath = "C:\\path\\to\\PlantVillage-Dataset\\raw\\color"  # Update this
$targetPath = "data\\PlantVillage"

# Copy images
$diseases = Get-ChildItem -Path $plantVillagePath -Directory
foreach ($disease in $diseases) {
    $targetFolder = Join-Path $targetPath $disease.Name
    if (Test-Path $targetFolder) {
        Copy-Item "$($disease.FullName)\\*" $targetFolder -Recurse
        Write-Host "Copied images to: $targetFolder"
    }
}
```

## Folder Mapping:

PlantVillage folders match your folder names:
- `Apple___Black_rot` → `data/PlantVillage/Apple___Black_rot/`
- `Tomato___Late_blight` → `data/PlantVillage/Tomato___Late_blight/`
- etc.

Just copy the images directly!
"""
    
    with open('PLANTVILLAGE_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Created PLANTVILLAGE_GUIDE.md")

if __name__ == "__main__":
    print("🌱 Creating Download Assistance Tools")
    print("=" * 50)
    
    create_google_images_urls()
    create_download_script()
    create_plantvillage_guide()
    
    print("\n✅ All helper files created!")
    print("\n📝 Recommended Approach:")
    print("1. BEST: Download PlantVillage dataset (see PLANTVILLAGE_GUIDE.md)")
    print("2. ALTERNATIVE: Use Google Images URLs (see google_images_urls.txt)")
    print("3. Check status: Run 'python download_disease_images.py'")
    print("4. Retrain: Run 'python train_model.py' after adding images")

