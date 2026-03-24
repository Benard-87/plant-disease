"""
Lightweight training script for Plant Disease Detection Model
Uses standalone Keras (already installed) without full TensorFlow overhead
"""

import os
import sys
import argparse
from pathlib import Path

# Use standalone Keras if TensorFlow not available
try:
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization, Input
    from tensorflow.keras.models import Model
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    import tensorflow as tf
    print("[OK] Using TensorFlow/Keras")
    USE_TF = True
except ImportError:
    # Fallback to standalone Keras
    from keras.applications import ResNet50
    from keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization, Input
    from keras.models import Model
    from keras.optimizers import Adam
    from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
    from keras.preprocessing.image import ImageDataGenerator
    print("[OK] Using standalone Keras (lightweight mode)")
    USE_TF = False

import numpy as np
import json
import matplotlib.pyplot as plt
from config import MODEL_CONFIG, MODEL_DIR

class PlantDiseaseModelLite:
    """Lightweight Plant Disease Detection Model using ResNet50"""
    
    def __init__(self, num_classes=38, input_shape=(224, 224, 3)):
        self.num_classes = num_classes
        self.input_shape = input_shape
        self.model = None
        self.history = None
        self.class_indices = None
    
    def build_model(self, freeze_base=True):
        """
        Build ResNet50 model with transfer learning
        
        Args:
            freeze_base (bool): Whether to freeze the base ResNet50 layers
        """
        print("[Building] Building ResNet50 model...")
        
        # Load pre-trained ResNet50 model
        base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=self.input_shape
        )
        
        # Freeze base model layers if specified
        if freeze_base:
            base_model.trainable = False
            print("   - Base model layers frozen")
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = BatchNormalization()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        
        # Create the final model
        self.model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile the model
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("   - Model compiled successfully")
        return self.model
    
    def train(self, train_generator, val_generator, epochs=50, verbose=1):
        """
        Train the model
        
        Args:
            train_generator: Training data generator
            val_generator: Validation data generator
            epochs (int): Number of training epochs
            verbose (int): Verbosity level
        """
        # Create callbacks
        callbacks = self._create_callbacks()
        
        # Train the model
        print(f"\n🚀 Starting training for {epochs} epochs...")
        self.history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=verbose
        )
        
        return self.history
    
    def _create_callbacks(self):
        """Create training callbacks"""
        callbacks = []
        
        # Model checkpoint
        checkpoint_path = os.path.join(MODEL_DIR, 'best_model.h5')
        checkpoint = ModelCheckpoint(
            checkpoint_path,
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            verbose=1
        )
        callbacks.append(checkpoint)
        
        # Early stopping
        early_stopping = EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        callbacks.append(early_stopping)
        
        # Learning rate reduction
        lr_reduction = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
        callbacks.append(lr_reduction)
        
        return callbacks
    
    def save_model(self, filepath=None):
        """
        Save the trained model
        
        Args:
            filepath (str): Path to save the model
        """
        if filepath is None:
            filepath = os.path.join(MODEL_DIR, 'plant_disease_model.h5')
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        print(f"[Saved] Model saved to {filepath}")
    
    def plot_training_history(self, save_path=None):
        """
        Plot training history
        
        Args:
            save_path (str): Path to save the plot
        """
        if self.history is None:
            print("No training history available")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        axes[0].plot(self.history.history['accuracy'], label='Training Accuracy')
        axes[0].plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        axes[0].set_title('Model Accuracy')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot loss
        axes[1].plot(self.history.history['loss'], label='Training Loss')
        axes[1].plot(self.history.history['val_loss'], label='Validation Loss')
        axes[1].set_title('Model Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"[Saved] Training history plot saved to {save_path}")
        
        plt.close()

def create_data_generators(data_dir, batch_size=32):
    """
    Create data generators for training and validation
    
    Args:
        data_dir (str): Path to the dataset directory
        batch_size (int): Batch size for data generators
        
    Returns:
        tuple: (train_generator, val_generator, class_indices)
    """
    print(f"\n[Creating] Creating data generators from {data_dir}...")
    
    # Enhanced data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        zoom_range=0.2,
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # No augmentation for validation
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    # Get class indices mapping
    class_indices = train_generator.class_indices
    
    return train_generator, val_generator, class_indices

def load_dataset_info(data_dir):
    """Load dataset information"""
    if not os.path.exists(data_dir):
        print(f"[ERROR] Dataset directory {data_dir} does not exist")
        return None
    
    # Get all class directories
    class_dirs = [d for d in os.listdir(data_dir) 
                 if os.path.isdir(os.path.join(data_dir, d))]
    
    class_dirs.sort()
    
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
        'class_counts': class_counts,
        'total_samples': total_samples
    }
    
    return dataset_info

def train_model(data_dir, epochs=50, batch_size=32):
    """
    Train the plant disease detection model
    
    Args:
        data_dir (str): Path to the dataset directory
        epochs (int): Number of training epochs
        batch_size (int): Batch size for training
    """
    
    print("Starting Plant Disease Detection Model Training (Lightweight)")
    print("=" * 60)
    
    # Check if dataset exists
    if not os.path.exists(data_dir):
        print(f"[ERROR] Dataset directory not found: {data_dir}")
        return
    
    # Load dataset info
    dataset_info = load_dataset_info(data_dir)
    if dataset_info is None:
        print("[ERROR] Failed to load dataset information")
        return
    
    print(f"\n[Dataset Information]")
    print(f"   - Number of classes: {dataset_info['num_classes']}")
    print(f"   - Total samples: {dataset_info['total_samples']}")
    print(f"   - Classes: {', '.join(dataset_info['class_names'][:5])}...")
    
    # Create data generators
    train_generator, val_generator, class_indices = create_data_generators(data_dir, batch_size=batch_size)
    
    num_classes = len(class_indices)
    print(f"   - Training batches: {len(train_generator)}")
    print(f"   - Validation batches: {len(val_generator)}")
    print(f"   - Classes detected: {num_classes}")
    
    # Save class indices mapping
    class_indices_path = os.path.join(MODEL_DIR, 'class_indices.json')
    with open(class_indices_path, 'w') as f:
        json.dump(class_indices, f, indent=2)
    print(f"   - Class indices saved to: {class_indices_path}")
    
    # Build model
    model = PlantDiseaseModelLite(num_classes=num_classes)
    model.build_model(freeze_base=True)
    
    # Print model summary
    print("\n📋 Model Summary:")
    model.model.summary()
    
    # Train model
    history = model.train(train_generator, val_generator, epochs=epochs)
    
    # Save model
    print("\n[Saving] Saving model...")
    model.save_model()
    
    # Plot training history
    print("\n[Plotting] Plotting training history...")
    plot_path = os.path.join(MODEL_DIR, 'training_history.png')
    model.plot_training_history(save_path=plot_path)
    
    print("\n[SUCCESS] Training completed successfully!")
    print(f"Model saved to: {MODEL_DIR}")
    print(f"Training history plot saved to: {plot_path}")

def main():
    """Main function with command line arguments"""
    
    parser = argparse.ArgumentParser(description='Train Plant Disease Detection Model (Lightweight)')
    parser.add_argument('--data_dir', type=str, 
                       default=os.path.join(os.path.dirname(__file__), 'data', 'PlantVillage'),
                       help='Path to the dataset directory')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for training')
    
    args = parser.parse_args()
    
    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Train model
    train_model(
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size
    )

if __name__ == "__main__":
    main()
