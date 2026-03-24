# Plant Disease Detection System - Training Improvements

## What Was Fixed

### 1. **Dynamic Class Detection**
- The model now automatically detects the number of disease classes from your dataset
- No longer hardcoded to 38 classes - adapts to your actual data
- Class mappings are saved in `models/class_indices.json`

### 2. **Added Anthracnose Support**
- Added "Anthracnose" to the disease classes
- Created directory: `data/PlantVillage/Anthracnose/`
- Added treatment recommendations for anthracnose

### 3. **Improved Data Augmentation**
- Enhanced augmentation with:
  - Rotation: 30 degrees (was 20)
  - Shifts: 30% (was 20%)
  - Vertical flips added
  - Brightness variation: 0.7-1.3
  - Better zoom and shear ranges

### 4. **Better Model Accuracy**
- Model now uses the correct number of classes from your dataset
- Improved training with better callbacks and learning rate scheduling
- Class indices are automatically saved and loaded

## How to Add More Disease Images

### For Anthracnose:
1. Place your anthracnose images in: `data/PlantVillage/Anthracnose/`
2. Or use the helper script:
   ```bash
   python add_anthracnose_image.py path/to/your/image.jpg
   ```

### For Other Diseases:
1. Create a folder in `data/PlantVillage/` with the disease name
2. Example: `data/PlantVillage/Leaf_Spot/`
3. Add images to that folder
4. The model will automatically detect the new class when you retrain

## Retraining the Model

The model is currently training with:
- 30 epochs
- Batch size: 16
- Enhanced data augmentation
- Dynamic class detection

After training completes:
1. The model will be saved to `models/plant_disease_model.h5`
2. Class indices will be saved to `models/class_indices.json`
3. Restart the Streamlit app to use the new model

## Important Notes

⚠️ **For Better Accuracy:**
- Add at least 20-30 images per disease class
- Use diverse images (different lighting, angles, severity)
- Ensure images are clear and show the disease symptoms well
- Balance the dataset (similar number of images per class)

⚠️ **Current Status:**
- The Anthracnose folder is created but empty
- You need to add anthracnose images to train the model to recognize it
- The model will work with whatever classes you have in your dataset

## Next Steps

1. **Add Anthracnose Images:**
   - Collect 20+ anthracnose leaf images
   - Add them to `data/PlantVillage/Anthracnose/`
   - Use the helper script or manually copy images

2. **Add More Disease Types (Optional):**
   - Create folders for other diseases you want to detect
   - Add images to each folder
   - The system will automatically include them

3. **Retrain:**
   - Run: `python train_model.py --data_dir "data/PlantVillage" --epochs 50 --batch_size 16`
   - Or use more epochs for better accuracy: `--epochs 100`

4. **Test:**
   - Restart Streamlit app
   - Upload images and test predictions
   - The model should now correctly identify anthracnose and other diseases

## Current Dataset Structure

```
data/PlantVillage/
├── Apple___Apple_scab/
├── Apple___healthy/
├── Potato___healthy/
├── Potato___Late_blight/
├── Tomato___Early_blight/
├── Tomato___healthy/
└── Anthracnose/  (NEW - add images here!)
```

The model will automatically detect all folders and create classes for each one!

