"""
Force cleanup - aggressively removes ALL subdirectories from disease folders
"""
import os
import shutil
from pathlib import Path

def force_cleanup():
    base_dir = Path("data/PlantVillage")
    if not base_dir.exists():
        print(f"Directory not found: {base_dir}")
        return
    
    print("=" * 60)
    print("FORCE CLEANUP: Removing ALL subdirectories")
    print("=" * 60)
    
    removed_count = 0
    total_folders = 0
    
    for disease_folder in base_dir.iterdir():
        if not disease_folder.is_dir():
            continue
        
        total_folders += 1
        print(f"\nProcessing: {disease_folder.name}")
        
        # Get all items in the folder
        items = list(disease_folder.iterdir())
        subdirs_removed = 0
        
        for item in items:
            if item.is_dir():
                try:
                    # Force remove with ignore_errors
                    shutil.rmtree(str(item), ignore_errors=True)
                    # Double check - if still exists, try again
                    if item.exists():
                        import time
                        time.sleep(0.1)
                        shutil.rmtree(str(item), ignore_errors=True)
                    
                    if not item.exists():
                        subdirs_removed += 1
                        removed_count += 1
                        print(f"  Removed: {item.name}")
                except Exception as e:
                    print(f"  [WARNING] Could not remove {item.name}: {e}")
        
        if subdirs_removed == 0:
            print(f"  No subdirectories found")
    
    print("\n" + "=" * 60)
    print(f"Cleanup complete!")
    print(f"  Processed: {total_folders} folders")
    print(f"  Removed: {removed_count} subdirectories")
    print("=" * 60)
    
    # Verify - check for any remaining subdirectories
    print("\nVerifying cleanup...")
    remaining = 0
    for disease_folder in base_dir.iterdir():
        if not disease_folder.is_dir():
            continue
        for item in disease_folder.iterdir():
            if item.is_dir():
                remaining += 1
                print(f"  [WARNING] Still exists: {disease_folder.name}/{item.name}")
    
    if remaining == 0:
        print("  [SUCCESS] All subdirectories removed!")
    else:
        print(f"  [WARNING] {remaining} subdirectories still remain")
        print("  You may need to manually delete them")

if __name__ == "__main__":
    force_cleanup()

