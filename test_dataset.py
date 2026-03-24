"""Quick test to check if dataset loads correctly"""
from data_preprocessing import DataPreprocessor
import os

print("Testing dataset loading...")
preprocessor = DataPreprocessor()
data_dir = 'data/PlantVillage'

if os.path.exists(data_dir):
    print(f"✓ Dataset directory exists: {data_dir}")
    info = preprocessor.load_dataset_info(data_dir)
    if info:
        print(f"✓ Dataset loaded successfully!")
        print(f"  - Number of classes: {info['num_classes']}")
        print(f"  - Total samples: {info['total_samples']}")
        print(f"  - Sample classes: {info['class_names'][:5]}")
    else:
        print("✗ Failed to load dataset info")
else:
    print(f"✗ Dataset directory not found: {data_dir}")


