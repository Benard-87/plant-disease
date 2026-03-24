# Using PlantVillage Dataset (RECOMMENDED)

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
$plantVillagePath = "C:\path\to\PlantVillage-Dataset\raw\color"  # Update this
$targetPath = "data\PlantVillage"

# Copy images
$diseases = Get-ChildItem -Path $plantVillagePath -Directory
foreach ($disease in $diseases) {
    $targetFolder = Join-Path $targetPath $disease.Name
    if (Test-Path $targetFolder) {
        Copy-Item "$($disease.FullName)\*" $targetFolder -Recurse
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
