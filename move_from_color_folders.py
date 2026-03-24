"""
Move images from nested 'color' subdirectories to main disease folders
PlantVillage dataset structure: Disease_Name/.../color/*.jpg
"""

from pathlib import Path
import shutil

def move_images_from_color_folders():
    """Move all images from 'color' subfolders to main disease folders"""
    base_dir = Path("data/PlantVillage")
    
    print("🌱 Moving images from 'color' subfolders to main folders")
    print("=" * 60)
    
    # Find all 'color' folders
    color_folders = list(base_dir.rglob('color'))
    
    if not color_folders:
        print("❌ No 'color' folders found")
        return
    
    print(f"Found {len(color_folders)} 'color' folders\n")
    
    total_moved = 0
    
    for color_folder in color_folders:
        # Get images in this color folder
        images = list(color_folder.glob('*.jpg')) + \
                 list(color_folder.glob('*.jpeg')) + \
                 list(color_folder.glob('*.png'))
        
        if not images:
            continue
        
        # Find the main disease folder (go up from color folder)
        # Structure: Disease_Name/.../color/
        current = color_folder.parent
        disease_folder = None
        
        # Go up until we find a folder that matches a disease name
        while current != base_dir and current != base_dir.parent:
            if current.parent == base_dir:
                disease_folder = current
                break
            current = current.parent
        
        if not disease_folder:
            # Try to find disease folder by name in parent path
            path_parts = color_folder.parts
            try:
                pv_index = path_parts.index('PlantVillage')
                if pv_index + 1 < len(path_parts):
                    disease_name = path_parts[pv_index + 1]
                    disease_folder = base_dir / disease_name
            except:
                pass
        
        if disease_folder and disease_folder.exists():
            print(f"📁 {disease_folder.name}: Moving {len(images)} images...")
            
            moved = 0
            for img in images:
                try:
                    dest = disease_folder / img.name
                    if dest.exists():
                        # Add counter if file exists
                        counter = 1
                        while dest.exists():
                            dest = disease_folder / f"{img.stem}_{counter}{img.suffix}"
                            counter += 1
                    
                    shutil.move(str(img), str(dest))
                    moved += 1
                except Exception as e:
                    print(f"   ⚠️ Error: {e}")
            
            total_moved += moved
            print(f"   ✅ Moved {moved} images")
        else:
            print(f"⚠️ Could not determine disease folder for: {color_folder}")
    
    print("\n" + "=" * 60)
    print(f"✅ Complete! Moved {total_moved} images")
    
    # Show final counts
    print("\n📊 Final image counts:")
    for disease_folder in sorted(base_dir.iterdir()):
        if disease_folder.is_dir():
            images = list(disease_folder.glob('*.jpg')) + \
                     list(disease_folder.glob('*.jpeg')) + \
                     list(disease_folder.glob('*.png'))
            # Only count images in root, not subdirectories
            root_images = [img for img in images if img.parent == disease_folder]
            if root_images:
                print(f"   - {disease_folder.name}: {len(root_images)} images")

if __name__ == "__main__":
    move_images_from_color_folders()

