"""
Quick script to check training status and model information
"""
import os
import json
from datetime import datetime

def check_status():
    print("=" * 60)
    print("TRAINING STATUS CHECK")
    print("=" * 60)
    
    # Check model file
    model_path = "models/plant_disease_model.h5"
    if os.path.exists(model_path):
        model_file = os.path.getmtime(model_path)
        model_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        model_time = datetime.fromtimestamp(model_file)
        age_minutes = (datetime.now() - model_time).total_seconds() / 60
        
        print(f"\n[Model File Status]")
        print(f"   Path: {model_path}")
        print(f"   Size: {model_size:.2f} MB")
        print(f"   Last Modified: {model_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Age: {age_minutes:.1f} minutes ago")
        
        if age_minutes < 10:
            print(f"   ⚡ Status: RECENTLY UPDATED - Training may be active!")
        else:
            print(f"   ⏸️  Status: Not updated recently")
    else:
        print(f"\n❌ Model file not found: {model_path}")
    
    # Check class indices
    class_indices_path = "models/class_indices.json"
    if os.path.exists(class_indices_path):
        with open(class_indices_path, 'r') as f:
            class_indices = json.load(f)
        print(f"\n[Class Indices]")
        print(f"   Total classes in JSON: {len(class_indices)}")
        print(f"   First 5 classes: {list(class_indices.keys())[:5]}")
    else:
        print(f"\n❌ Class indices file not found")
    
    # Check dataset
    data_dir = "data/PlantVillage"
    if os.path.exists(data_dir):
        folders = [d for d in os.listdir(data_dir) 
                  if os.path.isdir(os.path.join(data_dir, d))]
        print(f"\n[Dataset Status]")
        print(f"   Total classes in dataset: {len(folders)}")
        print(f"   Sample classes: {', '.join(sorted(folders)[:5])}")
    else:
        print(f"\n❌ Dataset directory not found: {data_dir}")
    
    # Check if we can load the model
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(model_path)
        num_classes = model.output_shape[-1]
        print(f"\n[Model Architecture]")
        print(f"   Output shape: {model.output_shape}")
        print(f"   Number of classes: {num_classes}")
        
        if num_classes == len(class_indices):
            print(f"   [OK] Model matches class indices count")
        else:
            print(f"   [WARNING] Model has {num_classes} classes but JSON has {len(class_indices)}")
            print(f"   This means the model needs retraining!")
    except Exception as e:
        print(f"\n❌ Error loading model: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_status()

