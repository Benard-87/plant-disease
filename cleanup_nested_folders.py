"""
Clean up nested subdirectories in PlantVillage dataset
Removes nested folder structures that cause training errors
"""
import os
import shutil
from pathlib import Path

def cleanup_nested_folders(base_dir="data/PlantVillage"):
    """Remove nested subdirectories from dataset folders"""
    
    print("=" * 60)
    print("Cleaning up nested subdirectories in dataset")
    print("=" * 60)
    
    if not os.path.exists(base_dir):
        print(f"[ERROR] Directory not found: {base_dir}")
        return
    
    base_path = Path(base_dir)
    removed_count = 0
    nested_folders = [
        'plant diseases names',
        'plantvillage dataset',
        'segmented',
        'grayscale',
        'color'
    ]
    
    # Get all disease class folders
    disease_folders = [d for d in base_path.iterdir() if d.is_dir()]
    print(f"\nFound {len(disease_folders)} disease class folders")
    
    for disease_folder in disease_folders:
        print(f"\nProcessing: {disease_folder.name}")
        
        # Remove known nested folder structures (force removal)
        for nested_name in nested_folders:
            nested_path = disease_folder / nested_name
            if nested_path.exists() and nested_path.is_dir():
                try:
                    print(f"  Removing: {nested_path}")
                    shutil.rmtree(str(nested_path), ignore_errors=True)
                    removed_count += 1
                except Exception as e:
                    print(f"  [WARNING] Could not remove {nested_path}: {e}")
        
        # Also remove any other subdirectories (keep only image files in root)
        for item in list(disease_folder.iterdir()):
            if item.is_dir():
                try:
                    print(f"  Removing nested directory: {item.name}")
                    shutil.rmtree(str(item), ignore_errors=True)
                    removed_count += 1
                except Exception as e:
                    print(f"  [WARNING] Could not remove {item}: {e}")
        
        # Check for any other nested directories that might contain images
        # We want images directly in the disease folder, not in subfolders
        for item in disease_folder.iterdir():
            if item.is_dir():
                # Check if this subdirectory contains image files
                has_images = any(f.suffix.lower() in ['.jpg', '.jpeg', '.png'] 
                               for f in item.rglob('*') if f.is_file())
                
                if has_images:
                    print(f"  [WARNING] Found nested directory with images: {item.name}")
                    print(f"    This may need manual cleanup")
    
    print("\n" + "=" * 60)
    print(f"Cleanup complete! Removed {removed_count} nested folders")
    print("=" * 60)
    
    # Verify structure
    print("\nVerifying dataset structure...")
    valid_folders = 0
    total_images = 0
    
    for disease_folder in disease_folders:
        # Count images directly in the folder (not in subdirectories)
        image_files = [f for f in disease_folder.iterdir() 
                      if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
        
        if len(image_files) > 0:
            valid_folders += 1
            total_images += len(image_files)
            print(f"  {disease_folder.name}: {len(image_files)} images")
    
    print(f"\n[Summary]")
    print(f"  Valid folders with images: {valid_folders}")
    print(f"  Total images found: {total_images}")
    print("=" * 60)

if __name__ == "__main__":
    cleanup_nested_folders()
