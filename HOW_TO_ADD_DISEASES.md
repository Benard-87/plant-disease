# How to Add New Plant Diseases

## ✅ YES - Create a Separate Folder for Each Disease!

The system works by organizing images into folders, where **each folder = one disease type**.

## Current Structure

```
data/PlantVillage/
├── Anthracnose/                    (empty - needs images!)
├── Apple___Apple_scab/             (20 images)
├── Apple___healthy/                 (20 images)
├── Potato___Late_blight/           (4 images)
├── Potato___healthy/                (20 images)
├── Tomato___Early_blight/          (20 images)
└── Tomato___healthy/                (20 images)
```

## How to Add a New Disease

### Step 1: Create a Folder
Create a new folder in `data/PlantVillage/` with the disease name:

**Examples:**
- `data/PlantVillage/Tomato___Late_blight/`
- `data/PlantVillage/Corn___Rust/`
- `data/PlantVillage/Leaf_Spot/`
- `data/PlantVillage/Powdery_Mildew/`
- `data/PlantVillage/Bacterial_Spot/`

### Step 2: Add Images
Add at least **20-30 images** of that disease to the folder.

**Image Requirements:**
- Clear, focused images showing the disease symptoms
- Different angles, lighting, and severity levels
- JPG, JPEG, or PNG format
- Recommended: 224x224 pixels or larger (will be resized automatically)

### Step 3: Retrain the Model
After adding images, retrain the model:

```bash
python train_model.py --data_dir "data/PlantVillage" --epochs 50 --batch_size 16
```

The model will **automatically detect** all folders and create classes for each one!

## Folder Naming Tips

### Good Folder Names:
- `Tomato___Late_blight` (clear, descriptive)
- `Apple___Black_rot` (specific)
- `Corn___Common_rust` (plant + disease)
- `Anthracnose` (if it affects multiple plants)

### Avoid:
- Spaces in names (use underscores: `_`)
- Special characters
- Very long names

## Example: Adding Multiple Diseases

Let's say you want to add 5 new diseases:

1. **Create folders:**
   ```
   data/PlantVillage/Tomato___Late_blight/
   data/PlantVillage/Corn___Rust/
   data/PlantVillage/Leaf_Spot/
   data/PlantVillage/Powdery_Mildew/
   data/PlantVillage/Bacterial_Spot/
   ```

2. **Add images to each folder** (20+ images per disease)

3. **Retrain:**
   ```bash
   python train_model.py --data_dir "data/PlantVillage" --epochs 50
   ```

4. **Result:** Model will now identify all 12 diseases (7 existing + 5 new)

## Quick Helper Script

You can use the helper script to add images:

```bash
# For anthracnose
python add_anthracnose_image.py path/to/your/image.jpg

# Or manually copy images to the folder
```

## Important Notes

⚠️ **Minimum Images:** At least 20 images per disease for decent accuracy  
⚠️ **More is Better:** 50-100 images per disease gives much better results  
⚠️ **Balance:** Try to have similar number of images per disease  
⚠️ **Quality:** Clear, well-lit images work best  

## Current Status

Your model is trained on **7 classes**:
1. Anthracnose (0 images - **needs data!**)
2. Apple___Apple_scab (20 images)
3. Apple___healthy (20 images)
4. Potato___Late_blight (4 images - **needs more!**)
5. Potato___healthy (20 images)
6. Tomato___Early_blight (20 images)
7. Tomato___healthy (20 images)

**Next Steps:**
1. Add images to `Anthracnose/` folder
2. Add more images to `Potato___Late_blight/` (only has 4!)
3. Add new disease folders as needed
4. Retrain the model

The system is **fully automatic** - just add folders and images, then retrain!

