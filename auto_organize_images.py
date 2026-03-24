"""
Automated script to organize PlantVillage images from subdirectories
Moves all images to the main disease folders
"""

import os
from pathlib import Path
import shutil

def organize_images_auto():
    """Automatically move images from subdirectories to main disease folders"""
    base_dir = Path("data/PlantVillage")
    
    print("🌱 Organizing PlantVillage Images")
    print("=" * 60)
    
    total_moved = 0
    folders_organized = []
    
    # Get all disease folders
    disease_folders = [d for d in base_dir.iterdir() if d.is_dir()]
    
    for disease_folder in disease_folders:
        # Find all images in this folder and subdirectories
        images = list(disease_folder.rglob("*.jpg")) + \
                 list(disease_folder.rglob("*.jpeg")) + \
                 list(disease_folder.rglob("*.png"))
        
        if not images:
            continue
        
        # Count images in root vs subdirectories
        root_images = [img for img in images if img.parent == disease_folder]
        subdir_images = [img for img in images if img.parent != disease_folder]
        
        if subdir_images:
            print(f"📁 {disease_folder.name}: Moving {len(subdir_images)} images from subdirectories...")
            
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
                    print(f"   ⚠️ Error moving {img.name}: {e}")
            
            total_moved += moved_count
            folders_organized.append((disease_folder.name, moved_count))
    
    print("\n" + "=" * 60)
    print(f"✅ Organization complete!")
    print(f"   - Folders organized: {len(folders_organized)}")
    print(f"   - Total images moved: {total_moved}")
    
    if folders_organized:
        print(f"\n📋 Summary:")
        for folder, count in folders_organized:
            print(f"   - {folder}: {count} images moved")
    
    # Now count final images
    print("\n📊 Final Image Count:")
    for disease_folder in sorted(disease_folders):
        images = list(disease_folder.glob("*.jpg")) + \
                 list(disease_folder.glob("*.jpeg")) + \
                 list(disease_folder.glob("*.png"))
        if images:
            print(f"   - {disease_folder.name}: {len(images)} images")

if __name__ == "__main__":
    organize_images_auto()

