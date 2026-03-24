"""
Comprehensive script to organize ALL PlantVillage images from subdirectories
Moves all images from nested folders to main disease folders
"""

from pathlib import Path
import shutil
import os
from collections import defaultdict

def organize_all_images():
    """Organize all images from subdirectories to main disease folders"""
    base_dir = Path("data/PlantVillage")
    
    print("🌱 Organizing ALL PlantVillage Images")
    print("=" * 70)
    
    # Step 1: Find all disease folders
    disease_folders = {d.name: d for d in base_dir.iterdir() if d.is_dir()}
    print(f"📁 Found {len(disease_folders)} disease folders\n")
    
    # Step 2: For each disease folder, find all images (including subdirectories)
    total_found = 0
    total_moved = 0
    folder_stats = {}
    
    for disease_name, disease_folder in disease_folders.items():
        print(f"📂 Processing: {disease_name}")
        
        # Find ALL images in this folder and all subdirectories
        all_images = list(disease_folder.rglob("*.jpg")) + \
                     list(disease_folder.rglob("*.jpeg")) + \
                     list(disease_folder.rglob("*.png"))
        
        if not all_images:
            print(f"   ⚠️ No images found")
            continue
        
        # Separate root images from subdirectory images
        root_images = [img for img in all_images if img.parent == disease_folder]
        subdir_images = [img for img in all_images if img.parent != disease_folder]
        
        print(f"   📊 Found {len(all_images)} total images")
        print(f"      - In root: {len(root_images)}")
        print(f"      - In subdirectories: {len(subdir_images)}")
        
        total_found += len(all_images)
        
        if subdir_images:
            print(f"   🔄 Moving {len(subdir_images)} images from subdirectories...")
            
            moved = 0
            skipped = 0
            errors = 0
            
            for img in subdir_images:
                try:
                    # Destination in main folder
                    dest = disease_folder / img.name
                    
                    # Handle duplicates
                    if dest.exists():
                        counter = 1
                        while dest.exists():
                            stem = img.stem
                            suffix = img.suffix
                            dest = disease_folder / f"{stem}_{counter}{suffix}"
                            counter += 1
                    
                    # Move the image
                    shutil.move(str(img), str(dest))
                    moved += 1
                    
                    # Progress indicator
                    if moved % 100 == 0:
                        print(f"      ... moved {moved}/{len(subdir_images)} images")
                        
                except shutil.Error:
                    # File already exists or can't move
                    skipped += 1
                except Exception as e:
                    errors += 1
                    if errors <= 5:  # Only show first 5 errors
                        print(f"      ⚠️ Error moving {img.name}: {e}")
            
            total_moved += moved
            folder_stats[disease_name] = {
                'total': len(all_images),
                'moved': moved,
                'skipped': skipped,
                'errors': errors,
                'final': len(root_images) + moved
            }
            
            print(f"   ✅ Moved {moved} images ({skipped} skipped, {errors} errors)")
        else:
            folder_stats[disease_name] = {
                'total': len(root_images),
                'moved': 0,
                'skipped': 0,
                'errors': 0,
                'final': len(root_images)
            }
            print(f"   ✅ Already organized ({len(root_images)} images in root)")
        
        print()
    
    # Step 3: Clean up empty subdirectories
    print("🧹 Cleaning up empty subdirectories...")
    cleaned = 0
    for disease_folder in disease_folders.values():
        for subdir in list(disease_folder.rglob('*')):
            if subdir.is_dir() and subdir != disease_folder:
                try:
                    # Check if empty
                    if not any(subdir.iterdir()):
                        subdir.rmdir()
                        cleaned += 1
                except:
                    pass
    
    print(f"   ✅ Removed {cleaned} empty subdirectories\n")
    
    # Step 4: Final summary
    print("=" * 70)
    print("📊 FINAL SUMMARY")
    print("=" * 70)
    print(f"Total images found: {total_found:,}")
    print(f"Total images moved: {total_moved:,}")
    print(f"Empty subdirectories removed: {cleaned}")
    
    print("\n📋 Per-Folder Summary:")
    print("-" * 70)
    print(f"{'Disease Folder':<40} {'Total':<10} {'Moved':<10} {'Final':<10}")
    print("-" * 70)
    
    for disease_name, stats in sorted(folder_stats.items()):
        if stats['final'] > 0:
            print(f"{disease_name:<40} {stats['total']:<10} {stats['moved']:<10} {stats['final']:<10}")
    
    # Step 5: Final image counts in root folders only
    print("\n" + "=" * 70)
    print("📸 FINAL IMAGE COUNTS (Root folders only):")
    print("=" * 70)
    
    total_final = 0
    folders_with_images = []
    
    for disease_name, disease_folder in sorted(disease_folders.items()):
        # Only count images in root (not subdirectories)
        root_images = list(disease_folder.glob("*.jpg")) + \
                      list(disease_folder.glob("*.jpeg")) + \
                      list(disease_folder.glob("*.png"))
        # Filter to only root level
        root_images = [img for img in root_images if img.parent == disease_folder]
        
        if root_images:
            count = len(root_images)
            total_final += count
            folders_with_images.append((disease_name, count))
            print(f"   ✅ {disease_name}: {count:,} images")
    
    print("\n" + "=" * 70)
    print(f"✅ Organization Complete!")
    print(f"   - Folders with images: {len(folders_with_images)}")
    print(f"   - Total images in root folders: {total_final:,}")
    print("\n💡 Next step: Retrain the model:")
    print("   python train_model.py --data_dir \"data/PlantVillage\" --epochs 50")

if __name__ == "__main__":
    print("\n⚠️  This will move ALL images from subdirectories to main folders")
    print("   Make sure you have a backup if needed!\n")
    
    response = input("Continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        organize_all_images()
    else:
        print("Cancelled.")

