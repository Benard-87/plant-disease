"""
Configuration file for Plant Disease Detection System
"""

import os

# Model Configuration
MODEL_CONFIG = {
    'input_size': (224, 224, 3),
    'num_classes': 38,  # PlantVillage dataset has 38 classes
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001,
    'dropout_rate': 0.5
}

# Data Configuration
DATA_CONFIG = {
    'train_split': 0.8,
    'val_split': 0.1,
    'test_split': 0.1,
    'augmentation_factor': 2
}

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
DATABASE_PATH = os.path.join(BASE_DIR, 'plant_disease.db')

# MySQL configuration (used if available)
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'database': 'plant_disease'
}

# Create directories if they don't exist
for directory in [DATA_DIR, MODEL_DIR, UPLOAD_DIR]:
    os.makedirs(directory, exist_ok=True)

# Disease classes mapping (PlantVillage dataset + additional diseases)
# This will be dynamically updated based on the dataset
DISEASE_CLASSES = {
    0: 'Apple___Apple_scab',
    1: 'Apple___Black_rot',
    2: 'Apple___Cedar_apple_rust',
    3: 'Apple___healthy',
    4: 'Blueberry___healthy',
    5: 'Cherry_(including_sour)___Powdery_mildew',
    6: 'Cherry_(including_sour)___healthy',
    7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    8: 'Corn_(maize)___Common_rust_',
    9: 'Corn_(maize)___Northern_Leaf_Blight',
    10: 'Corn_(maize)___healthy',
    11: 'Grape___Black_rot',
    12: 'Grape___Esca_(Black_Measles)',
    13: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    14: 'Grape___healthy',
    15: 'Orange___Haunglongbing_(Citrus_greening)',
    16: 'Peach___Bacterial_spot',
    17: 'Peach___healthy',
    18: 'Pepper,_bell___Bacterial_spot',
    19: 'Pepper,_bell___healthy',
    20: 'Potato___Early_blight',
    21: 'Potato___Late_blight',
    22: 'Potato___healthy',
    23: 'Raspberry___healthy',
    24: 'Soybean___healthy',
    25: 'Squash___Powdery_mildew',
    26: 'Strawberry___Leaf_scorch',
    27: 'Strawberry___healthy',
    28: 'Tomato___Bacterial_spot',
    29: 'Tomato___Early_blight',
    30: 'Tomato___Late_blight',
    31: 'Tomato___Leaf_Mold',
    32: 'Tomato___Septoria_leaf_spot',
    33: 'Tomato___Spider_mites Two-spotted_spider_mite',
    34: 'Tomato___Target_Spot',
    35: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    36: 'Tomato___Tomato_mosaic_virus',
    37: 'Tomato___healthy',
    # Additional common diseases
    38: 'Anthracnose',
    39: 'Leaf_Spot',
    40: 'Powdery_Mildew',
    41: 'Rust',
    42: 'Blight',
    43: 'Mosaic_Virus',
    44: 'Bacterial_Spot',
    45: 'Fungal_Infection'
}

def get_disease_classes_from_dataset(data_dir):
    """
    Dynamically get disease classes from the dataset directory structure
    
    Args:
        data_dir (str): Path to the dataset directory
        
    Returns:
        dict: Dictionary mapping class indices to class names
    """
    if not os.path.exists(data_dir):
        return DISEASE_CLASSES
    
    # Get all class directories
    class_dirs = [d for d in os.listdir(data_dir) 
                 if os.path.isdir(os.path.join(data_dir, d))]
    
    class_dirs.sort()  # Sort for consistent ordering
    
    # Create mapping
    class_mapping = {idx: cls for idx, cls in enumerate(class_dirs)}
    
    return class_mapping

# Treatment recommendations
TREATMENT_RECOMMENDATIONS = {
    'Apple___Apple_scab': {
        'description': 'Apple scab is a fungal disease that affects apple trees.',
        'treatment': [
            'Apply fungicide sprays in early spring',
            'Remove fallen leaves and debris',
            'Improve air circulation around trees',
            'Use resistant apple varieties'
        ],
        'prevention': 'Regular pruning and proper spacing of trees'
    },
    'Apple___Black_rot': {
        'description': 'Black rot is a fungal disease affecting apple fruits and leaves.',
        'treatment': [
            'Remove infected fruits and mummified apples',
            'Apply copper-based fungicides',
            'Prune infected branches',
            'Improve tree nutrition'
        ],
        'prevention': 'Good sanitation and proper tree care'
    },
    'Tomato___Early_blight': {
        'description': 'Early blight is a common fungal disease in tomatoes.',
        'treatment': [
            'Apply fungicide containing chlorothalonil or copper',
            'Remove infected leaves and stems',
            'Improve air circulation',
            'Water at soil level, not on leaves'
        ],
        'prevention': 'Crop rotation and proper spacing'
    },
    'Tomato___Late_blight': {
        'description': 'Late blight is a serious fungal disease that can destroy entire crops.',
        'treatment': [
            'Apply fungicide immediately when symptoms appear',
            'Remove and destroy infected plants',
            'Improve drainage and air circulation',
            'Use resistant varieties'
        ],
        'prevention': 'Avoid overhead watering and maintain good spacing'
    },
    'Potato___Early_blight': {
        'description': 'Early blight affects potato leaves and can reduce yield.',
        'treatment': [
            'Apply fungicide sprays',
            'Remove infected plant debris',
            'Improve soil drainage',
            'Use certified seed potatoes'
        ],
        'prevention': 'Crop rotation and proper field sanitation'
    },
    'Potato___Late_blight': {
        'description': 'Late blight is a devastating disease that can cause complete crop loss.',
        'treatment': [
            'Apply fungicide preventively',
            'Remove infected plants immediately',
            'Improve air circulation',
            'Use resistant varieties'
        ],
        'prevention': 'Regular monitoring and preventive fungicide application'
    },
    'Anthracnose': {
        'description': 'Anthracnose is a fungal disease that causes dark, sunken lesions on leaves, stems, and fruits.',
        'treatment': [
            'Remove and destroy infected plant parts immediately',
            'Apply copper-based fungicides or chlorothalonil',
            'Improve air circulation by pruning',
            'Avoid overhead watering',
            'Apply fungicide every 7-14 days during wet weather'
        ],
        'prevention': 'Use disease-free seeds, practice crop rotation, maintain proper spacing, and avoid working with plants when wet'
    },
    'Leaf_Spot': {
        'description': 'Leaf spot diseases cause circular or irregular spots on leaves, often leading to defoliation.',
        'treatment': [
            'Remove infected leaves',
            'Apply fungicide containing mancozeb or chlorothalonil',
            'Improve air circulation',
            'Water at the base of plants'
        ],
        'prevention': 'Good sanitation, proper spacing, and avoiding overhead irrigation'
    },
    'Powdery_Mildew': {
        'description': 'Powdery mildew appears as white powdery spots on leaves and stems.',
        'treatment': [
            'Apply sulfur-based fungicides',
            'Use neem oil or potassium bicarbonate',
            'Remove severely infected leaves',
            'Improve air circulation'
        ],
        'prevention': 'Plant resistant varieties, maintain proper spacing, and avoid overhead watering'
    }
}

# Default treatment for unknown diseases
DEFAULT_TREATMENT = {
    'description': 'General plant disease management',
    'treatment': [
        'Remove infected plant parts',
        'Improve air circulation',
        'Apply appropriate fungicide or pesticide',
        'Ensure proper nutrition and watering',
        'Consult with local agricultural extension service'
    ],
    'prevention': 'Regular monitoring, good sanitation, and proper plant care'
}
