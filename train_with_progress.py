"""
Training script with visible progress for Plant Disease Detection Model
Shows real-time training progress
"""
import os
import sys
import argparse
from pathlib import Path

# Set encoding to avoid Unicode issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
    from tensorflow.keras.models import Model
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    import tensorflow as tf
    print("[OK] Using TensorFlow/Keras")
    USE_TF = True
except ImportError as e:
    print(f"[ERROR] Failed to import TensorFlow: {e}")
    sys.exit(1)

import numpy as np
import json
import matplotlib.pyplot as plt
from config import MODEL_DIR

class ProgressCallback(tf.keras.callbacks.Callback):
    """Custom callback to show training progress"""
    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        acc = logs.get('accuracy', 0) * 100
        val_acc = logs.get('val_accuracy', 0) * 100
        loss = logs.get('loss', 0)
        val_loss = logs.get('val_loss', 0)
        
        print(f"\nEpoch {epoch + 1} Results:")
        print(f"  Training - Loss: {loss:.4f}, Accuracy: {acc:.2f}%")
        print(f"  Validation - Loss: {val_loss:.4f}, Accuracy: {val_acc:.2f}%")
        print("-" * 60)

def create_data_generators(data_dir, batch_size=32):
    """Create data generators for training and validation"""
    print(f"\n[Creating] Creating data generators from {data_dir}...")
    
    if not os.path.exists(data_dir):
        print(f"[ERROR] Dataset directory not found: {data_dir}")
        return None, None, None
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest',
        validation_split=0.2
    )
    
    # No augmentation for validation
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Create generators with error handling
    print("  Loading training data...")
    try:
        train_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True,
            follow_links=False  # Don't follow symlinks
        )
    except Exception as e:
        print(f"  [ERROR] Failed to create training generator: {e}")
        return None, None, None
    
    print("  Loading validation data...")
    try:
        val_generator = val_datagen.flow_from_directory(
            data_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False,
            follow_links=False  # Don't follow symlinks
        )
    except Exception as e:
        print(f"  [ERROR] Failed to create validation generator: {e}")
        return None, None, None
    
    class_indices = train_generator.class_indices
    print(f"  Found {len(class_indices)} classes")
    print(f"  Training samples: {train_generator.samples}")
    print(f"  Validation samples: {val_generator.samples}")
    
    return train_generator, val_generator, class_indices

def build_model(num_classes, input_shape=(224, 224, 3)):
    """Build ResNet50 model"""
    print(f"\n[Building] Building ResNet50 model for {num_classes} classes...")
    
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    base_model.trainable = False
    print("  Base ResNet50 layers frozen")
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("  Model compiled successfully")
    return model

def train_model(data_dir, epochs=10, batch_size=16):
    """Train the model with progress display"""
    
    print("=" * 60)
    print("PLANT DISEASE DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Create data generators
    train_gen, val_gen, class_indices = create_data_generators(data_dir, batch_size)
    
    if train_gen is None:
        print("[ERROR] Failed to create data generators")
        return
    
    num_classes = len(class_indices)
    print(f"\n[INFO] Training model with {num_classes} disease classes")
    
    # Build model
    model = build_model(num_classes)
    
    # Print model summary
    print("\n[Model Summary]")
    model.summary(print_fn=lambda x: print(f"  {x}"))
    
    # Setup callbacks
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    callbacks = [
        ModelCheckpoint(
            os.path.join(MODEL_DIR, 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        ),
        ProgressCallback(),
        CSVLogger(os.path.join(MODEL_DIR, 'training_log.csv'))
    ]
    
    # Train model
    print(f"\n[Training] Starting training for {epochs} epochs...")
    print("=" * 60)
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    print("\n[Saving] Saving final model...")
    model_path = os.path.join(MODEL_DIR, 'plant_disease_model.h5')
    model.save(model_path)
    print(f"  Model saved to: {model_path}")
    
    # Save class indices
    class_indices_path = os.path.join(MODEL_DIR, 'class_indices.json')
    with open(class_indices_path, 'w') as f:
        json.dump(class_indices, f, indent=2)
    print(f"  Class indices saved to: {class_indices_path}")
    
    # Plot training history
    print("\n[Plotting] Creating training history plot...")
    try:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        axes[0].plot(history.history['accuracy'], label='Training Accuracy')
        axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
        axes[0].set_title('Model Accuracy')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True)
        
        axes[1].plot(history.history['loss'], label='Training Loss')
        axes[1].plot(history.history['val_loss'], label='Validation Loss')
        axes[1].set_title('Model Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        plot_path = os.path.join(MODEL_DIR, 'training_history.png')
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Plot saved to: {plot_path}")
    except Exception as e:
        print(f"  Warning: Could not create plot: {e}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("[SUCCESS] Training completed!")
    print("=" * 60)
    print(f"Final Training Accuracy: {history.history['accuracy'][-1]*100:.2f}%")
    print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]*100:.2f}%")
    print(f"Model saved with {num_classes} classes")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train Plant Disease Detection Model with Progress')
    parser.add_argument('--data_dir', type=str, 
                       default=os.path.join(os.path.dirname(__file__), 'data', 'PlantVillage'),
                       help='Path to the dataset directory')
    parser.add_argument('--epochs', type=int, default=10,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=16,
                       help='Batch size for training')
    
    args = parser.parse_args()
    
    train_model(
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size
    )

