"""
Demo script for Plant Disease Detection System
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from model import PlantDiseaseModel
from data_preprocessing import DataPreprocessor
from treatment_recommender import TreatmentRecommender
from database import PlantDiseaseDB

def create_demo_image():
    """Create a demo plant leaf image"""
    # Create a simple demo image (green leaf-like shape)
    img = np.zeros((224, 224, 3), dtype=np.uint8)
    
    # Create a leaf-like shape
    center_x, center_y = 112, 112
    for y in range(224):
        for x in range(224):
            # Distance from center
            dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            # Create leaf shape
            if dist < 80 and abs(x - center_x) < 60:
                # Healthy green color
                img[y, x] = [34, 139, 34]  # Forest green
                
                # Add some texture
                if (x + y) % 10 < 3:
                    img[y, x] = [50, 205, 50]  # Lime green
            elif dist < 100 and abs(x - center_x) < 70:
                # Leaf edge
                img[y, x] = [0, 100, 0]  # Dark green
    
    return img

def create_diseased_demo_image():
    """Create a demo diseased plant leaf image"""
    # Create a simple demo image (brown/diseased leaf)
    img = np.zeros((224, 224, 3), dtype=np.uint8)
    
    # Create a leaf-like shape
    center_x, center_y = 112, 112
    for y in range(224):
        for x in range(224):
            # Distance from center
            dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            # Create diseased leaf shape
            if dist < 80 and abs(x - center_x) < 60:
                # Diseased brown color
                img[y, x] = [139, 69, 19]  # Saddle brown
                
                # Add disease spots
                if (x + y) % 15 < 5:
                    img[y, x] = [160, 82, 45]  # Sienna
            elif dist < 100 and abs(x - center_x) < 70:
                # Leaf edge
                img[y, x] = [101, 67, 33]  # Dark brown
    
    return img

def run_demo():
    """Run the complete demo"""
    print("Plant Disease Detection System - Demo")
    print("=" * 50)
    
    # Initialize components
    print("Initializing components...")
    model = PlantDiseaseModel()
    preprocessor = DataPreprocessor()
    recommender = TreatmentRecommender()
    database = PlantDiseaseDB()
    
    # Build and load model
    print("Building model...")
    model.build_model()
    
    # Create demo images
    print("Creating demo images...")
    healthy_img = create_demo_image()
    diseased_img = create_diseased_demo_image()
    
    # Save demo images
    os.makedirs('uploads', exist_ok=True)
    healthy_path = 'uploads/demo_healthy.jpg'
    diseased_path = 'uploads/demo_diseased.jpg'
    
    Image.fromarray(healthy_img).save(healthy_path)
    Image.fromarray(diseased_img).save(diseased_path)
    
    print(f"Demo images saved to {healthy_path} and {diseased_path}")
    
    # Test predictions
    print("\nTesting predictions...")
    
    # Test healthy image
    print("\n1. Testing 'healthy' leaf image:")
    processed_healthy = preprocessor.preprocess_image_from_array(healthy_img)
    if processed_healthy is not None:
        predicted_class, confidence, top_3 = model.predict(processed_healthy)
        print(f"   Predicted: {predicted_class}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Top 3: {top_3[:3]}")
        
        # Get treatment recommendation
        treatment = recommender.get_treatment_recommendation(predicted_class, confidence)
        print(f"   Treatment urgency: {treatment['urgency']}")
        
        # Log to database
        prediction_id = database.log_prediction(
            image_path=healthy_path,
            predicted_class=predicted_class,
            confidence=confidence,
            top_3_predictions=top_3,
            notes="Demo healthy leaf"
        )
        print(f"   Logged to database (ID: {prediction_id})")
    
    # Test diseased image
    print("\n2. Testing 'diseased' leaf image:")
    processed_diseased = preprocessor.preprocess_image_from_array(diseased_img)
    if processed_diseased is not None:
        predicted_class, confidence, top_3 = model.predict(processed_diseased)
        print(f"   Predicted: {predicted_class}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Top 3: {top_3[:3]}")
        
        # Get treatment recommendation
        treatment = recommender.get_treatment_recommendation(predicted_class, confidence)
        print(f"   Treatment urgency: {treatment['urgency']}")
        print(f"   Treatment steps: {len(treatment['treatment'])} steps available")
        
        # Log to database
        prediction_id = database.log_prediction(
            image_path=diseased_path,
            predicted_class=predicted_class,
            confidence=confidence,
            top_3_predictions=top_3,
            notes="Demo diseased leaf"
        )
        print(f"   Logged to database (ID: {prediction_id})")
    
    # Show database statistics
    print("\nDatabase Statistics:")
    stats = database.get_disease_statistics()
    print(f"   Total predictions: {stats['total_predictions']}")
    print(f"   Average confidence: {stats['average_confidence']:.2%}")
    print(f"   Unique diseases detected: {len(stats['disease_distribution'])}")
    
    # Show treatment recommendations
    print("\nSample Treatment Recommendations:")
    sample_diseases = ['Tomato___Early_blight', 'Apple___Apple_scab', 'Potato___Late_blight']
    
    for disease in sample_diseases:
        treatment = recommender.get_treatment_recommendation(disease)
        print(f"\n   {disease.replace('_', ' ').title()}:")
        print(f"   - Urgency: {treatment['urgency']}")
        print(f"   - Treatment steps: {len(treatment['treatment'])}")
        print(f"   - Description: {treatment['description'][:100]}...")
    
    # Show general plant care tips
    print("\nGeneral Plant Care Tips:")
    care_tips = recommender.get_general_plant_care_tips()
    for category, tips in list(care_tips.items())[:3]:  # Show first 3 categories
        print(f"\n   {category}:")
        for tip in tips[:2]:  # Show first 2 tips per category
            print(f"   - {tip}")
    
    print("\nDemo completed successfully!")
    print("\nTo run the web interface:")
    print("   streamlit run app.py")
    print("\nFor more information, see README.md")

def main():
    """Main demo function"""
    try:
        run_demo()
    except Exception as e:
        print(f"Demo failed with error: {str(e)}")
        print("Please check that all dependencies are installed correctly.")

if __name__ == "__main__":
    main()
