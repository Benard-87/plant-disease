"""
ResNet50 model implementation for Plant Disease Detection
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import plot_model
import matplotlib.pyplot as plt
from config import MODEL_CONFIG, MODEL_DIR, DISEASE_CLASSES
import json

class PlantDiseaseModel:
    """Plant Disease Detection Model using ResNet50"""
    
    def __init__(self, num_classes=38, input_shape=(224, 224, 3)):
        self.num_classes = num_classes
        self.input_shape = input_shape
        self.model = None
        self.history = None
        self.class_indices = None
        self._load_class_indices()
    
    def _load_class_indices(self):
        """Load class indices from saved JSON file if it exists"""
        class_indices_path = os.path.join(MODEL_DIR, 'class_indices.json')
        if os.path.exists(class_indices_path):
            try:
                with open(class_indices_path, 'r') as f:
                    class_to_idx = json.load(f)
                    # Reverse mapping: class_name -> index to index -> class_name
                    self.class_indices = {v: k for k, v in class_to_idx.items()}
                    print(f"Loaded class indices from {class_indices_path}")
            except Exception as e:
                print(f"Warning: Could not load class indices: {e}")
                self.class_indices = None
        else:
            self.class_indices = None
        
    def build_model(self, freeze_base=True):
        """
        Build ResNet50 model with transfer learning
        
        Args:
            freeze_base (bool): Whether to freeze the base ResNet50 layers
        """
        # Load pre-trained ResNet50 model
        base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=self.input_shape
        )
        
        # Freeze base model layers if specified
        if freeze_base:
            base_model.trainable = False
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = BatchNormalization()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(MODEL_CONFIG['dropout_rate'])(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(MODEL_CONFIG['dropout_rate'])(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        
        # Create the final model
        self.model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile the model
        self.model.compile(
            optimizer=Adam(learning_rate=MODEL_CONFIG['learning_rate']),
            loss='categorical_crossentropy',
            metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
        )
        
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
    
    def predict(self, image):
        """
        Make prediction on a single image
        
        Args:
            image (np.array): Preprocessed image array
            
        Returns:
            tuple: (predicted_class, confidence, all_predictions)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please load a trained model first.")
        
        # Make prediction
        predictions = self.model.predict(image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # IMPORTANT: Only use classes that the model was actually trained on
        # Get class name - use class_indices if available, otherwise fall back to DISEASE_CLASSES
        if self.class_indices is not None and len(self.class_indices) > 0:
            # Only use indices that exist in our trained classes
            if predicted_class_idx in self.class_indices:
                predicted_class = self.class_indices[predicted_class_idx]
            else:
                # If index is out of range, find the highest valid prediction
                valid_indices = [idx for idx in range(len(predictions[0])) if idx in self.class_indices]
                if valid_indices:
                    predicted_class_idx = max(valid_indices, key=lambda x: predictions[0][x])
                    predicted_class = self.class_indices[predicted_class_idx]
                    confidence = float(predictions[0][predicted_class_idx])
                else:
                    predicted_class = f"Class_{predicted_class_idx}"
        else:
            # Fallback to DISEASE_CLASSES but only for valid indices
            if predicted_class_idx < len(DISEASE_CLASSES):
                predicted_class = DISEASE_CLASSES.get(predicted_class_idx, f"Class_{predicted_class_idx}")
            else:
                predicted_class = f"Class_{predicted_class_idx}"
        
        # Get top 3 predictions - only from valid classes
        if self.class_indices is not None and len(self.class_indices) > 0:
            # Only consider classes that were actually trained
            valid_predictions = [(idx, float(predictions[0][idx])) for idx in self.class_indices.keys()]
            valid_predictions.sort(key=lambda x: x[1], reverse=True)
            top_3_predictions = [(self.class_indices[idx], conf) for idx, conf in valid_predictions[:3]]
        else:
            # Fallback: get top 3 from all predictions
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            top_3_predictions = []
            for idx in top_3_indices:
                if idx < len(DISEASE_CLASSES):
                    class_name = DISEASE_CLASSES.get(idx, f"Class_{idx}")
                else:
                    class_name = f"Class_{idx}"
                confidence_score = float(predictions[0][idx])
                top_3_predictions.append((class_name, confidence_score))
        
        return predicted_class, confidence, top_3_predictions
    
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
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath=None):
        """
        Load a trained model
        
        Args:
            filepath (str): Path to the model file
        """
        if filepath is None:
            filepath = os.path.join(MODEL_DIR, 'plant_disease_model.h5')
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        self.model = tf.keras.models.load_model(filepath)
        # Reload class indices after loading model
        self._load_class_indices()
        print(f"Model loaded from {filepath}")
    
    def plot_training_history(self, save_path=None):
        """
        Plot training history
        
        Args:
            save_path (str): Path to save the plot
        """
        if self.history is None:
            print("No training history available")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Training Accuracy')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Plot loss
        axes[0, 1].plot(self.history.history['loss'], label='Training Loss')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation Loss')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Plot top-3 accuracy
        if 'top_3_accuracy' in self.history.history:
            axes[1, 0].plot(self.history.history['top_3_accuracy'], label='Training Top-3 Accuracy')
            axes[1, 0].plot(self.history.history['val_top_3_accuracy'], label='Validation Top-3 Accuracy')
            axes[1, 0].set_title('Top-3 Accuracy')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Top-3 Accuracy')
            axes[1, 0].legend()
            axes[1, 0].grid(True)
        
        # Plot learning rate
        if 'lr' in self.history.history:
            axes[1, 1].plot(self.history.history['lr'])
            axes[1, 1].set_title('Learning Rate')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Learning Rate')
            axes[1, 1].set_yscale('log')
            axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Training history plot saved to {save_path}")
        
        plt.show()
    
    def get_model_summary(self):
        """Get model summary"""
        if self.model is None:
            print("Model not built yet")
            return
        
        self.model.summary()
    
    def fine_tune(self, train_generator, val_generator, epochs=20, learning_rate=1e-5):
        """
        Fine-tune the model by unfreezing some layers
        
        Args:
            train_generator: Training data generator
            val_generator: Validation data generator
            epochs (int): Number of fine-tuning epochs
            learning_rate (float): Learning rate for fine-tuning
        """
        if self.model is None:
            raise ValueError("Model not built yet")
        
        # Unfreeze some layers for fine-tuning
        for layer in self.model.layers[-20:]:  # Unfreeze last 20 layers
            layer.trainable = True
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
        )
        
        # Fine-tune
        self.history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=self._create_callbacks(),
            verbose=1
        )
        
        return self.history

def create_pretrained_model():
    """Create a pre-trained model for demonstration purposes"""
    model = PlantDiseaseModel()
    model.build_model(freeze_base=True)
    return model

def main():
    """Test the model functionality"""
    # Create model
    model = PlantDiseaseModel()
    model.build_model()
    
    # Print model summary
    print("Model Summary:")
    model.get_model_summary()
    
    # Create a dummy model for demonstration
    print("\nCreating a dummy trained model for demonstration...")
    model.save_model()

if __name__ == "__main__":
    main()
