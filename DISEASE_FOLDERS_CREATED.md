# Disease Folders Created

I've created folders for **15 additional common plant diseases**. Here's what's now set up:

## All Disease Folders (22 Total)

### Existing (7):
1. ✅ `Anthracnose/` (empty - needs images)
2. ✅ `Apple___Apple_scab/` (20 images)
3. ✅ `Apple___healthy/` (20 images)
4. ✅ `Potato___Late_blight/` (4 images)
5. ✅ `Potato___healthy/` (20 images)
6. ✅ `Tomato___Early_blight/` (20 images)
7. ✅ `Tomato___healthy/` (20 images)

### Newly Created (15):
8. 🆕 `Apple___Black_rot/` (empty - needs images)
9. 🆕 `Apple___Cedar_apple_rust/` (empty - needs images)
10. 🆕 `Cherry_Powdery_mildew/` (empty - needs images)
11. 🆕 `Corn___Common_rust/` (empty - needs images)
12. 🆕 `Corn___Northern_Leaf_Blight/` (empty - needs images)
13. 🆕 `Grape___Black_rot/` (empty - needs images)
14. 🆕 `Grape___Leaf_blight/` (empty - needs images)
15. 🆕 `Pepper_bell___Bacterial_spot/` (empty - needs images)
16. 🆕 `Potato___Early_blight/` (empty - needs images)
17. 🆕 `Squash___Powdery_mildew/` (empty - needs images)
18. 🆕 `Tomato___Bacterial_spot/` (empty - needs images)
19. 🆕 `Tomato___Late_blight/` (empty - needs images)
20. 🆕 `Tomato___Leaf_Mold/` (empty - needs images)
21. 🆕 `Tomato___Septoria_leaf_spot/` (empty - needs images)
22. 🆕 `Tomato___Target_Spot/` (empty - needs images)

## Next Steps

### 1. Add Images to Each Folder
For each disease folder, add **20-30 images** (or more for better accuracy):
- Clear images showing disease symptoms
- Different angles and lighting
- JPG, JPEG, or PNG format

### 2. Retrain the Model
After adding images, retrain:

```bash
python train_model.py --data_dir "data/PlantVillage" --epochs 50 --batch_size 16
```

The model will automatically detect all folders and create classes for each one!

### 3. Priority Folders
Start with these if you have limited images:
- `Anthracnose/` (you mentioned this earlier)
- `Tomato___Late_blight/` (common disease)
- `Potato___Early_blight/` (complements your existing Potato___Late_blight)
- `Apple___Black_rot/` (complements your existing Apple___Apple_scab)

## Current Status

**Total Folders:** 22  
**Folders with Images:** 6 (with varying amounts)  
**Empty Folders:** 16 (ready for images)

Once you add images and retrain, your model will be able to identify **all 22 disease types**!

## Quick Add Script

You can use the helper script to add images:

```bash
# For any disease, just copy images to the folder
# Example: Copy images to data/PlantVillage/Tomato___Late_blight/
```

Or manually drag and drop images into each folder.

