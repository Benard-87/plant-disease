"""
Fix PlantVillage dataset structure
The dataset has nested folders - this script organizes them properly
"""

from pathlib import Path
import shutil

def find_and_organize_images():
    """Find images in nested structure and organize them"""
    base_dir = Path("data/PlantVillage")
    
    print("🔍 Scanning for images in nested structure...")
    print("=" * 60)
    
    # Find all directories with images
    all_dirs = []
    for root, dirs, files in base_dir.rglob('*'):
        root_path = Path(root)
        images = list(root_path.glob('*.jpg')) + list(root_path.glob('*.jpeg')) + list(root_path.glob('*.png'))
        if images and root_path.is_dir():
            all_dirs.append((root_path, len(images)))
    
    print(f"Found {len(all_dirs)} directories with images")
    print("\nTop 20 directories with images:")
    for dir_path, count in sorted(all_dirs, key=lambda x: x[1], reverse=True)[:20]:
        rel_path = dir_path.relative_to(base_dir)
        print(f"  {rel_path}: {count} images")
    
    # Check if images are in nested "color" folders (PlantVillage structure)
    print("\n" + "=" * 60)
    print("Checking for PlantVillage 'color' folder structure...")
    
    color_folders = list(base_dir.rglob('color'))
    if color_folders:
        print(f"Found {len(color_folders)} 'color' folders")
        for color_folder in color_folders[:5]:
            parent = color_folder.parent
            images = list(color_folder.glob('*.jpg')) + list(color_folder.glob('*.jpeg')) + list(color_folder.glob('*.png'))
            print(f"  {parent.relative_to(base_dir)}/color: {len(images)} images")
    
    print("\n" + "=" * 60)
    print("💡 Solution:")
    print("The PlantVillage dataset has images in nested 'color' subdirectories.")
    print("You need to:")
    print("1. Find the 'color' folder in each disease folder")
    print("2. Move images from 'color' subfolder to the main disease folder")
    print("\nOr the images might be organized by disease name in the nested structure.")
    print("Run this to see the full structure:")
    print("  Get-ChildItem 'data\\PlantVillage' -Recurse -Directory | Where-Object { $_.Name -eq 'color' }")

if __name__ == "__main__":
    find_and_organize_images()

