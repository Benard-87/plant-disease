"""
Quick cleanup - removes all subdirectories from disease folders
Only keeps image files directly in each disease folder
"""
import os
import shutil
from pathlib import Path

def quick_cleanup():
    base_dir = Path("data/PlantVillage")
    if not base_dir.exists():
        print(f"Directory not found: {base_dir}")
        return
    
    print("Quick cleanup: Removing all subdirectories from disease folders...")
    removed = 0
    
    for disease_folder in base_dir.iterdir():
        if not disease_folder.is_dir():
            continue
        
        for item in list(disease_folder.iterdir()):
            if item.is_dir():
                try:
                    shutil.rmtree(str(item), ignore_errors=True)
                    removed += 1
                    print(f"Removed: {disease_folder.name}/{item.name}")
                except:
                    pass
    
    print(f"\nDone! Removed {removed} nested directories.")
    print("Now run: python train_with_progress.py --epochs 10 --batch_size 16")

if __name__ == "__main__":
    quick_cleanup()

