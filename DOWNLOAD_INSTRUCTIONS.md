
# How to Download Plant Disease Images

## Method 1: Manual Download (Recommended)
1. Go to Google Images: https://images.google.com
2. Search for each disease (see search terms below)
3. Filter by "Usage rights" -> "Labeled for reuse"
4. Download 20-30 images per disease
5. Save them to the corresponding folder in data/PlantVillage/

## Method 2: Use PlantVillage Dataset (Best Quality)
The PlantVillage dataset is the best source for plant disease images:
- Website: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- Or: https://github.com/spMohanty/PlantVillage-Dataset
- Contains thousands of labeled plant disease images
- Free to use for research/educational purposes

## Method 3: Use Browser Extension
- Install "Image Downloader" extension for Chrome/Firefox
- Search Google Images with filters
- Bulk download images
- Organize into folders

## Search Terms for Each Disease:

- Anthracnose: Search 'anthracnose plant disease'
- Apple___Black_rot: Search 'apple black rot disease'
- Apple___Cedar_apple_rust: Search 'apple cedar rust disease'
- Corn___Common_rust: Search 'corn common rust disease'
- Corn___Cercospora_leaf_spot: Search 'corn cercospora leaf spot'
- Corn___Northern_Leaf_Blight: Search 'corn northern leaf blight'
- Corn___healthy: Search 'healthy corn plant'
- Grape___Black_rot: Search 'grape black rot disease'
- Grape___Esca: Search 'grape esca disease'
- Grape___Leaf_blight: Search 'grape leaf blight disease'
- Grape___healthy: Search 'healthy grape plant'
- Pepper_bell___Bacterial_spot: Search 'pepper bacterial spot disease'
- Pepper_bell___healthy: Search 'healthy bell pepper plant'
- Cherry_Powdery_mildew: Search 'cherry powdery mildew disease'
- Cherry_healthy: Search 'healthy cherry plant'
- Strawberry___Leaf_scorch: Search 'strawberry leaf scorch disease'
- Strawberry___healthy: Search 'healthy strawberry plant'
- Peach___Bacterial_spot: Search 'peach bacterial spot disease'
- Peach___healthy: Search 'healthy peach plant'
- Blueberry___healthy: Search 'healthy blueberry plant'
- Orange___Haunglongbing: Search 'citrus greening disease'
- Soybean___healthy: Search 'healthy soybean plant'
- Raspberry___healthy: Search 'healthy raspberry plant'
- Squash___Powdery_mildew: Search 'squash powdery mildew disease'
- Squash___healthy: Search 'healthy squash plant'
- Tomato___Bacterial_spot: Search 'tomato bacterial spot disease'
- Tomato___Late_blight: Search 'tomato late blight disease'
- Tomato___Leaf_Mold: Search 'tomato leaf mold disease'
- Tomato___Septoria_leaf_spot: Search 'tomato septoria leaf spot disease'
- Tomato___Spider_mites: Search 'tomato spider mites damage'
- Tomato___Target_Spot: Search 'tomato target spot disease'
- Tomato___Tomato_mosaic_virus: Search 'tomato mosaic virus disease'
- Tomato___Tomato_Yellow_Leaf_Curl_Virus: Search 'tomato yellow leaf curl virus'
- Potato___Early_blight: Search 'potato early blight disease'

## Image Requirements:
- Format: JPG, JPEG, or PNG
- Size: At least 224x224 pixels (larger is better)
- Quality: Clear, focused images showing disease symptoms
- Quantity: 20-50 images per disease for good accuracy

## After Downloading:
1. Place images in: data/PlantVillage/[Disease_Name]/
2. Retrain model: python train_model.py --data_dir "data/PlantVillage" --epochs 50
