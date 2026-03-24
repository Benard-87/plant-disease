# PowerShell script to help organize downloaded images
# Run this after downloading images to organize them

$baseDir = "data\PlantVillage"

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
