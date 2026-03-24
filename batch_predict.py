"""
Batch prediction script for Plant Disease Detection System
"""

import os
import argparse
import pandas as pd
from PIL import Image
import numpy as np
from model import PlantDiseaseModel
from data_preprocessing import DataPreprocessor
from treatment_recommender import TreatmentRecommender
from database import PlantDiseaseDB

def batch_predict(input_dir, output_file, model_path=None):
    """
    Perform batch prediction on multiple images
    
    Args:
        input_dir (str): Directory containing images to predict
        output_file (str): Output CSV file path
        model_path (str): Path to trained model
    """
    
    print("🌱 Batch Plant Disease Detection")
    print("=" * 40)
    
    # Initialize components
    model = PlantDiseaseModel()
    preprocessor = DataPreprocessor()
    recommender = TreatmentRecommender()
    database = PlantDiseaseDB()
    
    # Load model
    if model_path and os.path.exists(model_path):
        model.load_model(model_path)
    else:
        print("⚠️ No trained model found. Using demonstration mode.")
        model.build_model()
    
    # Get image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = []
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(root, file))
    
    if not image_files:
        print(f"❌ No image files found in {input_dir}")
        return
    
    print(f"📁 Found {len(image_files)} images to process")
    
    # Process images
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"🔍 Processing {i}/{len(image_files)}: {os.path.basename(image_path)}")
        
        try:
            # Preprocess image
            processed_image = preprocessor.preprocess_image(image_path)
            
            if processed_image is not None:
                # Make prediction
                predicted_class, confidence, top_3_predictions = model.predict(processed_image)
                
                # Get treatment recommendation
                treatment = recommender.get_treatment_recommendation(predicted_class, confidence)
                
                # Store results
                result = {
                    'image_path': image_path,
                    'image_name': os.path.basename(image_path),
                    'predicted_class': predicted_class,
                    'confidence': confidence,
                    'confidence_percentage': f"{confidence:.2%}",
                    'top_2_class': top_3_predictions[1][0] if len(top_3_predictions) > 1 else '',
                    'top_2_confidence': top_3_predictions[1][1] if len(top_3_predictions) > 1 else 0,
                    'top_3_class': top_3_predictions[2][0] if len(top_3_predictions) > 2 else '',
                    'top_3_confidence': top_3_predictions[2][1] if len(top_3_predictions) > 2 else 0,
                    'treatment_urgency': treatment['urgency'],
                    'treatment_steps_count': len(treatment['treatment']),
                    'disease_description': treatment['description'][:100] + '...' if treatment['description'] else ''
                }
                
                results.append(result)
                
                # Log to database
                database.log_prediction(
                    image_path=image_path,
                    predicted_class=predicted_class,
                    confidence=confidence,
                    top_3_predictions=top_3_predictions,
                    notes="Batch prediction"
                )
                
                print(f"   ✅ {predicted_class} ({confidence:.2%})")
                
            else:
                print(f"   ❌ Failed to process image")
                results.append({
                    'image_path': image_path,
                    'image_name': os.path.basename(image_path),
                    'predicted_class': 'ERROR',
                    'confidence': 0,
                    'error': 'Failed to process image'
                })
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({
                'image_path': image_path,
                'image_name': os.path.basename(image_path),
                'predicted_class': 'ERROR',
                'confidence': 0,
                'error': str(e)
            })
    
    # Save results to CSV
    if results:
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        print(f"\n✅ Results saved to {output_file}")
        
        # Print summary
        successful_predictions = df[df['predicted_class'] != 'ERROR']
        if not successful_predictions.empty:
            print(f"\n📊 Summary:")
            print(f"   - Total images processed: {len(results)}")
            print(f"   - Successful predictions: {len(successful_predictions)}")
            print(f"   - Average confidence: {successful_predictions['confidence'].mean():.2%}")
            
            # Most common predictions
            top_predictions = successful_predictions['predicted_class'].value_counts().head(5)
            print(f"\n   Top 5 predicted diseases:")
            for disease, count in top_predictions.items():
                print(f"   - {disease.replace('_', ' ').title()}: {count} images")
        
        # Show high confidence predictions
        high_conf = successful_predictions[successful_predictions['confidence'] >= 0.8]
        if not high_conf.empty:
            print(f"\n   High confidence predictions (≥80%): {len(high_conf)}")
        
        # Show low confidence predictions
        low_conf = successful_predictions[successful_predictions['confidence'] < 0.5]
        if not low_conf.empty:
            print(f"   Low confidence predictions (<50%): {len(low_conf)}")
            print("   ⚠️ Consider manual review for low confidence predictions")
    
    else:
        print("❌ No results to save")

def main():
    """Main function with command line arguments"""
    
    parser = argparse.ArgumentParser(description='Batch Plant Disease Detection')
    parser.add_argument('--input_dir', type=str, required=True,
                       help='Directory containing images to predict')
    parser.add_argument('--output_file', type=str, default='batch_predictions.csv',
                       help='Output CSV file path')
    parser.add_argument('--model_path', type=str, default=None,
                       help='Path to trained model file')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"❌ Input directory not found: {args.input_dir}")
        return
    
    # Create output directory if needed
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Run batch prediction
    batch_predict(args.input_dir, args.output_file, args.model_path)

if __name__ == "__main__":
    main()
