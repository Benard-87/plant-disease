"""
Data preprocessing utilities for Plant Disease Detection System
"""

import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from config import MODEL_CONFIG, DATA_CONFIG, DISEASE_CLASSES

class DataPreprocessor:
    """Handles data preprocessing for plant disease detection"""
    
    def __init__(self):
        self.input_size = MODEL_CONFIG['input_size'][:2]  # (224, 224)
        self.num_classes = MODEL_CONFIG['num_classes']
        
    def preprocess_image(self, image_path):
        """
        Preprocess a single image for prediction
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            np.array: Preprocessed image array
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize image
            image = cv2.resize(image, self.input_size)
            
            # Normalize pixel values to [0, 1]
            image = image.astype(np.float32) / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            print(f"Error preprocessing image {image_path}: {str(e)}")
            return None
    
    def preprocess_image_from_array(self, image_array):
        """
        Preprocess image from numpy array
        
        Args:
            image_array (np.array): Image array
            
        Returns:
            np.array: Preprocessed image array
        """
        try:
            # Convert to RGB if needed
            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                # Assume it's already RGB
                pass
            elif len(image_array.shape) == 3 and image_array.shape[2] == 4:
                # Convert RGBA to RGB
                image_array = image_array[:, :, :3]
            
            # Resize image
            image = cv2.resize(image_array, self.input_size)
            
            # Normalize pixel values to [0, 1]
            image = image.astype(np.float32) / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            print(f"Error preprocessing image array: {str(e)}")
            return None
    
    def create_data_generators(self, data_dir, batch_size=32):
        """
        Create data generators for training and validation
        
        Args:
            data_dir (str): Path to the dataset directory
            batch_size (int): Batch size for data generators
            
        Returns:
            tuple: (train_generator, val_generator, class_indices)
        """
        # Enhanced data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=30,
            width_shift_range=0.3,
            height_shift_range=0.3,
            horizontal_flip=True,
            vertical_flip=True,
            zoom_range=0.3,
            shear_range=0.2,
            brightness_range=[0.7, 1.3],
            fill_mode='nearest',
            validation_split=0.2
        )
        
        # No augmentation for validation and test
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.2
        )
        
        # Create generators
        train_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=self.input_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        val_generator = val_datagen.flow_from_directory(
            data_dir,
            target_size=self.input_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        # Get class indices mapping
        class_indices = train_generator.class_indices
        
        return train_generator, val_generator, class_indices
    
    def load_dataset_info(self, data_dir):
        """
        Load dataset information and create class mapping
        
        Args:
            data_dir (str): Path to the dataset directory
            
        Returns:
            dict: Dataset information
        """
        if not os.path.exists(data_dir):
            print(f"Dataset directory {data_dir} does not exist")
            return None
        
        # Get all class directories
        class_dirs = [d for d in os.listdir(data_dir) 
                     if os.path.isdir(os.path.join(data_dir, d))]
        
        class_dirs.sort()  # Sort for consistent ordering
        
        # Create class mapping
        class_to_idx = {cls: idx for idx, cls in enumerate(class_dirs)}
        idx_to_class = {idx: cls for cls, idx in class_to_idx.items()}
        
        # Count samples per class
        class_counts = {}
        total_samples = 0
        
        for class_name in class_dirs:
            class_path = os.path.join(data_dir, class_name)
            count = len([f for f in os.listdir(class_path) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            class_counts[class_name] = count
            total_samples += count
        
        dataset_info = {
            'num_classes': len(class_dirs),
            'class_names': class_dirs,
            'class_to_idx': class_to_idx,
            'idx_to_class': idx_to_class,
            'class_counts': class_counts,
            'total_samples': total_samples
        }
        
        return dataset_info
    
    def create_sample_dataset(self, output_dir, num_samples_per_class=10):
        """
        Create a small sample dataset for testing purposes
        
        Args:
            output_dir (str): Output directory for sample dataset
            num_samples_per_class (int): Number of sample images per class
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create sample images for a few classes
        sample_classes = [
            'Apple___healthy',
            'Apple___Apple_scab',
            'Tomato___healthy',
            'Tomato___Early_blight',
            'Potato___healthy',
            'Potato___Late_blight'
        ]
        
        for class_name in sample_classes:
            class_dir = os.path.join(output_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            
            # Create sample images (colored rectangles for demonstration)
            for i in range(num_samples_per_class):
                # Create a random colored image
                img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
                
                # Add some variation based on class
                if 'healthy' in class_name:
                    # Greenish tint for healthy
                    img[:, :, 1] = np.clip(img[:, :, 1] + 50, 0, 255)
                else:
                    # Brownish tint for diseased
                    img[:, :, 0] = np.clip(img[:, :, 0] + 30, 0, 255)
                    img[:, :, 2] = np.clip(img[:, :, 2] - 20, 0, 255)
                
                # Save image
                img_pil = Image.fromarray(img)
                img_path = os.path.join(class_dir, f'sample_{i:03d}.jpg')
                img_pil.save(img_path)
        
        print(f"Created sample dataset in {output_dir}")
        print(f"Classes: {sample_classes}")
        print(f"Samples per class: {num_samples_per_class}")

def main():
    """Test the data preprocessing functionality"""
    preprocessor = DataPreprocessor()
    
    # Create sample dataset for testing
    sample_dir = os.path.join(os.path.dirname(__file__), 'data', 'sample_dataset')
    preprocessor.create_sample_dataset(sample_dir, num_samples_per_class=5)
    
    # Test dataset info loading
    dataset_info = preprocessor.load_dataset_info(sample_dir)
    if dataset_info:
        print("\nDataset Information:")
        print(f"Number of classes: {dataset_info['num_classes']}")
        print(f"Total samples: {dataset_info['total_samples']}")
        print("Class distribution:")
        for class_name, count in dataset_info['class_counts'].items():
            print(f"  {class_name}: {count} samples")

if __name__ == "__main__":
    main()
