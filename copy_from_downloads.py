"""
Copy PlantVillage images from Downloads folder to project data folder
"""

from pathlib import Path
import shutil

def copy_plantvillage_images():
    """Copy images from Downloads PlantVillage to project folders"""
    source_dir = Path(r"C:\Users\Benard\Downloads\plant diseases names\plantvillage dataset\color")
    target_dir = Path("data/PlantVillage")
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    print("🌱 Copying PlantVillage Images from Downloads")
    print("=" * 70)
    print(f"Source: {source_dir}")
    print(f"Target: {target_dir}")
    print()
    
    # Get all disease folders from source
    source_folders = [d for d in source_dir.iterdir() if d.is_dir()]
    print(f"📁 Found {len(source_folders)} disease folders in source\n")
    
    total_copied = 0
    folders_copied = []
    folders_skipped = []
    
    # Folder name mapping (handle slight differences)
    name_mapping = {
        'Cherry_(including_sour)___healthy': 'Cherry_healthy',
        'Cherry_(including_sour)___Powdery_mildew': 'Cherry_Powdery_mildew',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Corn___Cercospora_leaf_spot',
        'Corn_(maize)___Common_rust_': 'Corn___Common_rust',
        'Corn_(maize)___healthy': 'Corn___healthy',
        'Corn_(maize)___Northern_Leaf_Blight': 'Corn___Northern_Leaf_Blight',
        'Grape___Esca_(Black_Measles)': 'Grape___Esca',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Grape___Leaf_blight',
        'Orange___Haunglongbing_(Citrus_greening)': 'Orange___Haunglongbing',
        'Pepper,_bell___Bacterial_spot': 'Pepper_bell___Bacterial_spot',
        'Pepper,_bell___healthy': 'Pepper_bell___healthy',
        'Tomato___Spider_mites Two-spotted_spider_mite': 'Tomato___Spider_mites',
    }
    
    for source_folder in sorted(source_folders):
        source_name = source_folder.name
        
        # Map to target folder name
        target_name = name_mapping.get(source_name, source_name)
        target_folder = target_dir / target_name
        
        # Get images from source
        images = list(source_folder.glob("*.jpg")) + \
                 list(source_folder.glob("*.jpeg")) + \
                 list(source_folder.glob("*.png"))
        
        if not images:
            print(f"⚠️ {source_name}: No images found")
            folders_skipped.append(source_name)
            continue
        
        # Create target folder if it doesn't exist
        target_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"📂 {target_name}: Copying {len(images)} images...")
        
        copied = 0
        skipped = 0
        errors = 0
        
        for img in images:
            try:
                dest = target_folder / img.name
                
                # Skip if already exists
                if dest.exists():
                    skipped += 1
                    continue
                
                # Copy the image
                shutil.copy2(str(img), str(dest))
                copied += 1
                
                # Progress indicator
                if copied % 100 == 0:
                    print(f"   ... copied {copied}/{len(images)} images")
                    
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"   ⚠️ Error copying {img.name}: {e}")
        
        total_copied += copied
        folders_copied.append((target_name, copied, skipped))
        
        if skipped > 0:
            print(f"   ✅ Copied {copied} images ({skipped} already existed, {errors} errors)")
        else:
            print(f"   ✅ Copied {copied} images ({errors} errors)")
        print()
    
    # Final summary
    print("=" * 70)
    print("📊 COPY SUMMARY")
    print("=" * 70)
    print(f"Total images copied: {total_copied:,}")
    print(f"Folders processed: {len(folders_copied)}")
    print(f"Folders skipped (no images): {len(folders_skipped)}")
    
    print("\n📋 Folders Copied:")
    print("-" * 70)
    print(f"{'Disease Folder':<45} {'Copied':<10} {'Skipped':<10}")
    print("-" * 70)
    
    for folder_name, copied, skipped in sorted(folders_copied):
        print(f"{folder_name:<45} {copied:<10} {skipped:<10}")
    
    # Final image counts
    print("\n" + "=" * 70)
    print("📸 FINAL IMAGE COUNTS:")
    print("=" * 70)
    
    total_final = 0
    for disease_folder in sorted(target_dir.iterdir()):
        if disease_folder.is_dir():
            images = list(disease_folder.glob("*.jpg")) + \
                     list(disease_folder.glob("*.jpeg")) + \
                     list(disease_folder.glob("*.png"))
            # Only count root level
            root_images = [img for img in images if img.parent == disease_folder]
            if root_images:
                count = len(root_images)
                total_final += count
                print(f"   ✅ {disease_folder.name}: {count:,} images")
    
    print(f"\n   Total: {total_final:,} images across {len([d for d in target_dir.iterdir() if d.is_dir() and list((target_dir / d.name).glob('*.jpg'))])} folders")
    
    print("\n💡 Next step: Retrain the model:")
    print("   python train_model.py --data_dir \"data/PlantVillage\" --epochs 50")

if __name__ == "__main__":
    copy_plantvillage_images()

