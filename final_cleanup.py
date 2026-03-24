"""
Final cleanup - Remove ALL nested subdirectories from disease folders
Only keep images in the root of each disease folder
"""

from pathlib import Path
import shutil

def final_cleanup():
    """Remove all nested subdirectories"""
    base_dir = Path("data/PlantVillage")
    
    print("🧹 Final Cleanup - Removing ALL nested subdirectories")
    print("=" * 60)
    
    removed_count = 0
    
    for disease_folder in base_dir.iterdir():
        if not disease_folder.is_dir():
            continue
        
        # Find all subdirectories (not root level files)
        subdirs_to_remove = []
        for item in disease_folder.iterdir():
            if item.is_dir():
                subdirs_to_remove.append(item)
        
        # Remove each subdirectory
        for subdir in subdirs_to_remove:
            try:
                shutil.rmtree(str(subdir))
                removed_count += 1
                print(f"✅ Removed: {disease_folder.name}/{subdir.name}")
            except Exception as e:
                print(f"⚠️ Error removing {subdir}: {e}")
    
    print(f"\n✅ Cleanup complete! Removed {removed_count} nested folders")
    print("\n💡 Now training should work properly!")
    print("   Run: python train_model.py --data_dir \"data/PlantVillage\" --epochs 50 --batch_size 32")

if __name__ == "__main__":
    final_cleanup()

