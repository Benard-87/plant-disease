"""
Training script for Plant Disease Detection Model
"""

import os
import sys
import argparse
from model import PlantDiseaseModel
from data_preprocessing import DataPreprocessor
from config import MODEL_CONFIG, DATA_CONFIG, MODEL_DIR, get_disease_classes_from_dataset
import json

def train_model(data_dir, epochs=50, batch_size=32, fine_tune=False):
    """
    Train the plant disease detection model
    
    Args:
        data_dir (str): Path to the dataset directory
        epochs (int): Number of training epochs
        batch_size (int): Batch size for training
        fine_tune (bool): Whether to perform fine-tuning
    """
    
    print("🌱 Starting Plant Disease Detection Model Training")
    print("=" * 50)
    import sys
    sys.stdout.flush()
    
    # Initialize components
    print("Initializing components...")
    sys.stdout.flush()
    preprocessor = DataPreprocessor()
    model = PlantDiseaseModel()
    print("Components initialized!")
    sys.stdout.flush()
    
    # Check if dataset exists
    if not os.path.exists(data_dir):
        print(f"❌ Dataset directory not found: {data_dir}")
        print("Creating sample dataset for demonstration...")
        preprocessor.create_sample_dataset(data_dir, num_samples_per_class=20)
    
    # Load dataset info
    dataset_info = preprocessor.load_dataset_info(data_dir)
    if dataset_info is None:
        print("❌ Failed to load dataset information")
        return
    
    print(f"📊 Dataset Information:")
    print(f"   - Number of classes: {dataset_info['num_classes']}")
    print(f"   - Total samples: {dataset_info['total_samples']}")
    print(f"   - Classes: {', '.join(dataset_info['class_names'][:5])}...")
    
    # Create data generators
    print("\n🔄 Creating data generators...")
    train_generator, val_generator, class_indices = preprocessor.create_data_generators(
        data_dir, batch_size=batch_size
    )
    
    # Get actual number of classes from the generator
    num_classes = len(class_indices)
    print(f"   - Number of classes detected: {num_classes}")
    print(f"   - Classes: {list(class_indices.keys())}")
    print(f"   - Training batches: {len(train_generator)}")
    print(f"   - Validation batches: {len(val_generator)}")
    
    # Update model with correct number of classes
    model.num_classes = num_classes
    
    # Save class indices mapping for later use
    class_indices_path = os.path.join(MODEL_DIR, 'class_indices.json')
    with open(class_indices_path, 'w') as f:
        json.dump(class_indices, f, indent=2)
    print(f"   - Class indices saved to: {class_indices_path}")
    
    # Build model
    print("\n🏗️ Building model...")
    model.build_model(freeze_base=True)
    
    print("📋 Model Summary:")
    model.get_model_summary()
    
    # Train model
    print(f"\n🚀 Starting training for {epochs} epochs...")
    history = model.train(
        train_generator, 
        val_generator, 
        epochs=epochs
    )
    
    # Fine-tuning (optional)
    if fine_tune:
        print("\n🔧 Starting fine-tuning...")
        model.fine_tune(
            train_generator, 
            val_generator, 
            epochs=20,
            learning_rate=1e-5
        )
    
    # Save model
    print("\n💾 Saving model...")
    model.save_model()
    
    # Plot training history
    print("\n📈 Plotting training history...")
    plot_path = os.path.join(MODEL_DIR, 'training_history.png')
    model.plot_training_history(save_path=plot_path)
    
    print("\n✅ Training completed successfully!")
    print(f"Model saved to: {MODEL_DIR}")
    print(f"Training history plot saved to: {plot_path}")

def main():
    """Main function with command line arguments"""
    
    parser = argparse.ArgumentParser(description='Train Plant Disease Detection Model')
    parser.add_argument('--data_dir', type=str, 
                       default=os.path.join(os.path.dirname(__file__), 'data', 'PlantVillage'),
                       help='Path to the dataset directory')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for training')
    parser.add_argument('--fine_tune', action='store_true',
                       help='Perform fine-tuning after initial training')
    
    args = parser.parse_args()
    
    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Train model
    train_model(
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        fine_tune=args.fine_tune
    )

if __name__ == "__main__":
    main()
