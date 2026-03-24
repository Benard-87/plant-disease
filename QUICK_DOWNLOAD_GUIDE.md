# Quick Guide: Downloading Plant Disease Images

## ⚠️ Important Note
I cannot directly download images from the internet, but I've created tools to help you do it efficiently!

## 🎯 Best Methods (In Order of Quality)

### 1. **PlantVillage Dataset** (RECOMMENDED - Best Quality)
**Why:** Professional, labeled, high-quality images
- **Kaggle:** https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- **GitHub:** https://github.com/spMohanty/PlantVillage-Dataset
- Contains 54,000+ images across 38 disease classes
- Already organized by disease type
- Free for research/educational use

**How to use:**
1. Download the dataset
2. Extract images
3. Copy images to corresponding folders in `data/PlantVillage/`

### 2. **Google Images** (Manual - Most Flexible)
**Steps:**
1. Go to https://images.google.com
2. Search for each disease (see search terms below)
3. Click "Tools" → "Usage rights" → "Labeled for reuse"
4. Download 20-30 images per disease
5. Save to: `data/PlantVillage/[Disease_Folder]/`

**Search Terms:**
- Anthracnose: "anthracnose plant disease leaf"
- Apple Black Rot: "apple black rot disease"
- Tomato Late Blight: "tomato late blight disease"
- (See DOWNLOAD_INSTRUCTIONS.md for full list)

### 3. **Browser Extension** (Semi-Automated)
**Extensions:**
- "Image Downloader" for Chrome
- "Download All Images" for Firefox

**Steps:**
1. Install extension
2. Search Google Images with usage rights filter
3. Use extension to bulk download
4. Organize into folders

## 📁 Folder Structure

All images go into: `data/PlantVillage/[Disease_Name]/`

Example:
```
data/PlantVillage/
├── Anthracnose/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Tomato___Late_blight/
│   ├── image1.jpg
│   └── ...
```

## 📊 Current Status

Run this to check:
```bash
python download_disease_images.py
```

## ✅ Image Requirements

- **Format:** JPG, JPEG, or PNG
- **Size:** At least 224x224 pixels (larger is better)
- **Quality:** Clear, focused, showing disease symptoms
- **Quantity:** 20-50 images per disease minimum
- **Variety:** Different angles, lighting, severity levels

## 🚀 After Adding Images

1. **Check status:**
   ```bash
   python download_disease_images.py
   ```

2. **Retrain model:**
   ```bash
   python train_model.py --data_dir "data/PlantVillage" --epochs 50
   ```

3. **Test in app:**
   ```bash
   streamlit run app.py
   ```

## 💡 Pro Tips

1. **Start with PlantVillage dataset** - it's the easiest and highest quality
2. **Focus on 5-10 diseases first** - get those working well
3. **Balance your dataset** - similar number of images per disease
4. **Quality over quantity** - 20 clear images > 50 blurry ones
5. **Add gradually** - retrain after each batch of new images

## 🔗 Useful Resources

- **PlantVillage Dataset:** https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- **Plant Disease Images:** https://www.plantwise.org/knowledgebank
- **USDA Plant Database:** https://www.ars.usda.gov/

## ⚡ Quick Start (PlantVillage Method)

1. Download PlantVillage dataset from Kaggle
2. Extract to a temporary folder
3. Copy images to your `data/PlantVillage/` folders:
   - `PlantVillage/Apple___Black_rot/*` → `data/PlantVillage/Apple___Black_rot/`
   - `PlantVillage/Tomato___Late_blight/*` → `data/PlantVillage/Tomato___Late_blight/`
   - etc.
4. Run: `python train_model.py --data_dir "data/PlantVillage" --epochs 50`

That's it! The model will automatically detect all folders with images.

