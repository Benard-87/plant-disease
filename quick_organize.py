"""
Quick image organizer - simpler version
Run this if you want to organize images interactively
"""

from pathlib import Path
import shutil

def quick_organize():
    """Quickly organize images from subdirectories"""
    base_dir = Path("data/PlantVillage")
    
    print("🌱 Quick Image Organizer")
    print("=" * 60)
    
    total_moved = 0
    
    for disease_folder in sorted(base_dir.iterdir()):
        if not disease_folder.is_dir():
            continue
        
        # Find images in subdirectories only
        subdir_images = []
        for subdir in disease_folder.rglob('*'):
            if subdir.is_dir() and subdir != disease_folder:
                images = list(subdir.glob('*.jpg')) + \
                         list(subdir.glob('*.jpeg')) + \
                         list(subdir.glob('*.png'))
                subdir_images.extend(images)
        
        if subdir_images:
            print(f"📁 {disease_folder.name}: Moving {len(subdir_images)} images...")
            
            moved = 0
            for img in subdir_images:
                try:
                    dest = disease_folder / img.name
                    if dest.exists():
                        counter = 1
                        while dest.exists():
                            dest = disease_folder / f"{img.stem}_{counter}{img.suffix}"
                            counter += 1
                    shutil.move(str(img), str(dest))
                    moved += 1
                except:
                    pass
            
            total_moved += moved
            print(f"   ✅ Moved {moved} images")
    
    print(f"\n✅ Done! Moved {total_moved} images total")

if __name__ == "__main__":
    quick_organize()

