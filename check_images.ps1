# PowerShell script to help organize downloaded images
# After downloading images from Google/PlantVillage, use this to organize them

$downloadsFolder = "$env:USERPROFILE\Downloads"  # Change if your downloads are elsewhere
$targetBase = "data\PlantVillage"

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
Write-Host "2. Copy images to: $targetBase\[Disease_Folder]\"
Write-Host "3. Run this script again to check status"
