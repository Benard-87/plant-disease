"""
Script to organize PlantVillage images from subdirectories to main folders
PlantVillage dataset sometimes has nested folder structures
"""

import os
from pathlib import Path
import shutil

def organize_images():
    """Move images from subdirectories to main disease folders"""
    base_dir = Path("data/PlantVillage")
    
    print("🔍 Scanning for images in subdirectories...")
    print("=" * 60)
    
    total_moved = 0
    folders_organized = []
    
    # Get all disease folders
    disease_folders = [d for d in base_dir.iterdir() if d.is_dir()]
    
    for disease_folder in disease_folders:
        print(f"\n📁 Checking: {disease_folder.name}")
        
        # Find all images in this folder and subdirectories
        images = list(disease_folder.rglob("*.jpg")) + \
                 list(disease_folder.rglob("*.jpeg")) + \
                 list(disease_folder.rglob("*.png"))
        
        if not images:
            print(f"   ❌ No images found")
            continue
        
        # Count images in root vs subdirectories
        root_images = [img for img in images if img.parent == disease_folder]
        subdir_images = [img for img in images if img.parent != disease_folder]
        
        print(f"   📊 Found {len(images)} total images")
        print(f"      - In root: {len(root_images)}")
        print(f"      - In subdirectories: {len(subdir_images)}")
        
        if subdir_images:
            print(f"   🔄 Moving {len(subdir_images)} images from subdirectories...")
            
            # Move images from subdirectories to root
            moved_count = 0
            for img in subdir_images:
                try:
                    # Create unique filename if needed
                    dest = disease_folder / img.name
                    if dest.exists():
                        # Add number suffix if file exists
                        counter = 1
                        while dest.exists():
                            stem = img.stem
                            suffix = img.suffix
                            dest = disease_folder / f"{stem}_{counter}{suffix}"
                            counter += 1
                    
                    shutil.move(str(img), str(dest))
                    moved_count += 1
                except Exception as e:
                    print(f"      ⚠️ Error moving {img.name}: {e}")
            
            total_moved += moved_count
            print(f"   ✅ Moved {moved_count} images to root folder")
            folders_organized.append(disease_folder.name)
            
            # Remove empty subdirectories
            for subdir in disease_folder.iterdir():
                if subdir.is_dir():
                    try:
                        if not any(subdir.iterdir()):
                            subdir.rmdir()
                            print(f"   🗑️ Removed empty subdirectory: {subdir.name}")
                    except:
                        pass
    
    print("\n" + "=" * 60)
    print(f"✅ Organization complete!")
    print(f"   - Folders organized: {len(folders_organized)}")
    print(f"   - Total images moved: {total_moved}")
    
    if folders_organized:
        print(f"\n📋 Organized folders:")
        for folder in folders_organized:
            print(f"   - {folder}")

if __name__ == "__main__":
    print("🌱 PlantVillage Image Organizer")
    print("=" * 60)
    print("This script will move images from subdirectories to main folders")
    print()
    
    response = input("Continue? (y/n): ")
    if response.lower() == 'y':
        organize_images()
        print("\n✅ Done! Images are now organized in main folders.")
        print("You can now retrain the model.")
    else:
        print("Cancelled.")

