"""
Script to clean up nested folders and start training
Run this in VS Code terminal
"""

from pathlib import Path
import shutil
import subprocess
import sys

def cleanup_and_train():
    """Clean up nested folders and start training"""
    base_dir = Path("data/PlantVillage")
    
    print("🧹 Step 1: Cleaning up nested subdirectories...")
    print("=" * 60)
    
    removed = 0
    
    for disease_folder in base_dir.iterdir():
        if not disease_folder.is_dir():
            continue
        
        # Remove known nested folder structures
        for subdir_name in ['segmented', 'grayscale', 'color', 'plant diseases names', 'plantvillage dataset']:
            subdir = disease_folder / subdir_name
            if subdir.exists() and subdir.is_dir():
                try:
                    shutil.rmtree(str(subdir))
                    removed += 1
                    print(f"✅ Removed: {disease_folder.name}/{subdir_name}")
                except Exception as e:
                    print(f"⚠️ Error removing {subdir}: {e}")
    
    print(f"\n✅ Cleanup complete! Removed {removed} nested folders\n")
    
    print("🚀 Step 2: Starting training...")
    print("=" * 60)
    print("Training will start now. You can monitor progress in VS Code terminal.")
    print()
    
    # Run training
    try:
        subprocess.run([
            sys.executable, 
            "train_model.py",
            "--data_dir", "data/PlantVillage",
            "--epochs", "50",
            "--batch_size", "32"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Training failed with error: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⚠️ Training interrupted by user")
        return False
    
    print("\n✅ Training completed successfully!")
    return True

if __name__ == "__main__":
    cleanup_and_train()

