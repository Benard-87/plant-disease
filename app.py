"""
Streamlit Web Interface for Plant Disease Detection System
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import os
import tempfile
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Import our custom modules
from model import PlantDiseaseModel
from data_preprocessing import DataPreprocessor
from database import PlantDiseaseDB
from treatment_recommender import TreatmentRecommender
from config import DISEASE_CLASSES, MODEL_DIR

# Page configuration
st.set_page_config(
    page_title="Plant Disease Detection System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 1rem 0;
    }
    .treatment-card {
        background-color: #fff8dc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffa500;
        margin: 1rem 0;
    }
    .confidence-high { color: #228B22; }
    .confidence-medium { color: #FF8C00; }
    .confidence-low { color: #DC143C; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the plant disease detection model"""
    try:
        with st.spinner("Loading model... This may take a moment on first run."):
            model_path = os.path.join(MODEL_DIR, 'plant_disease_model.h5')
            class_indices_path = os.path.join(MODEL_DIR, 'class_indices.json')
            
            if os.path.exists(model_path):
                # Load the model first to check its actual output shape
                import tensorflow as tf
                temp_model = tf.keras.models.load_model(model_path)
                actual_num_classes = temp_model.output_shape[-1]
                del temp_model  # Free memory
                
                # Load class indices
                class_indices_dict = {}
                if os.path.exists(class_indices_path):
                    import json
                    with open(class_indices_path, 'r') as f:
                        class_indices_dict = json.load(f)
                
                # Create model with correct number of classes
                model = PlantDiseaseModel(num_classes=actual_num_classes)
                model.load_model(model_path)
                
                # Filter class_indices to only include classes the model was trained on
                if model.class_indices is not None:
                    # Only keep indices that are within the model's output range
                    filtered_indices = {idx: name for idx, name in model.class_indices.items() 
                                      if idx < actual_num_classes}
                    model.class_indices = filtered_indices
                elif class_indices_dict:
                    # If class_indices weren't loaded, create from JSON but filter to model size
                    filtered_indices = {}
                    for class_name, idx in class_indices_dict.items():
                        if idx < actual_num_classes:
                            filtered_indices[idx] = class_name
                    model.class_indices = filtered_indices
            else:
                # No model exists, determine num_classes from class_indices.json
                num_classes = 7  # default
                if os.path.exists(class_indices_path):
                    import json
                    with open(class_indices_path, 'r') as f:
                        class_indices = json.load(f)
                        num_classes = len(class_indices)
                
                # Create a model for demonstration
                st.info("No trained model found. Building new model...")
                model = PlantDiseaseModel(num_classes=num_classes)
                model.build_model()
                # Save the model so it can be loaded next time
                model.save_model()
        
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

@st.cache_resource
def load_components():
    """Load all system components"""
    preprocessor = DataPreprocessor()
    database = PlantDiseaseDB()
    recommender = TreatmentRecommender()
    return preprocessor, database, recommender

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🌱 Plant Disease Detection System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load components
    model = load_model()
    preprocessor, database, recommender = load_components()
    
    if model is None:
        st.error("Failed to load the model. Please check the model files.")
        return
    
    # Sidebar
    st.sidebar.title("🔧 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home - Disease Detection", "📊 Analytics Dashboard", "🌿 Treatment Guide", "📝 Database Management"]
    )
    
    if page == "🏠 Home - Disease Detection":
        disease_detection_page(model, preprocessor, database, recommender)
    elif page == "📊 Analytics Dashboard":
        analytics_dashboard(database)
    elif page == "🌿 Treatment Guide":
        treatment_guide_page(recommender)
    elif page == "📝 Database Management":
        database_management_page(database)

def disease_detection_page(model, preprocessor, database, recommender):
    """Main disease detection page"""
    
    st.header("🔍 Plant Disease Detection")
    st.markdown("Upload an image of a plant leaf to detect diseases and get treatment recommendations.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of a plant leaf for disease detection"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Image info
            st.info(f"**Image Details:**\n- Format: {image.format}\n- Size: {image.size}\n- Mode: {image.mode}")
        
        with col2:
            st.subheader("🔬 Analysis")
            
            # Process image
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("Analyzing image..."):
                    try:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                            image.save(tmp_file.name)
                            
                            # Preprocess image
                            processed_image = preprocessor.preprocess_image(tmp_file.name)
                            
                            if processed_image is not None:
                                # Make prediction
                                predicted_class, confidence, top_3_predictions = model.predict(processed_image)
                                
                                # Display results
                                display_prediction_results(
                                    predicted_class, confidence, top_3_predictions,
                                    tmp_file.name, database, recommender
                                )
                            else:
                                st.error("Failed to process the image. Please try a different image.")
                        
                        # Clean up temporary file
                        os.unlink(tmp_file.name)
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")

def display_prediction_results(predicted_class, confidence, top_3_predictions, image_path, database, recommender):
    """Display prediction results"""
    
    # Confidence styling
    if confidence >= 0.8:
        conf_class = "confidence-high"
    elif confidence >= 0.6:
        conf_class = "confidence-medium"
    else:
        conf_class = "confidence-low"
    
    # Main prediction card
    st.markdown(f"""
    <div class="prediction-card">
        <h3>🎯 Prediction Results</h3>
        <p><strong>Disease:</strong> {predicted_class.replace('_', ' ').title()}</p>
        <p><strong>Confidence:</strong> <span class="{conf_class}">{confidence:.2%}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top 3 predictions
    st.subheader("📊 Top 3 Predictions")
    pred_data = []
    for i, (class_name, conf) in enumerate(top_3_predictions):
        pred_data.append({
            'Rank': i + 1,
            'Disease': class_name.replace('_', ' ').title(),
            'Confidence': f"{conf:.2%}"
        })
    
    pred_df = pd.DataFrame(pred_data)
    st.dataframe(pred_df, use_container_width=True)
    
    # Confidence visualization
    fig = go.Figure(data=[
        go.Bar(
            x=[p[0].replace('_', ' ').title() for p in top_3_predictions],
            y=[p[1] for p in top_3_predictions],
            marker_color=['#2E8B57', '#FF8C00', '#DC143C']
        )
    ])
    fig.update_layout(
        title="Confidence Scores",
        xaxis_title="Disease",
        yaxis_title="Confidence",
        yaxis=dict(range=[0, 1])
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Treatment recommendations
    st.subheader("💊 Treatment Recommendations")
    treatment_info = recommender.get_treatment_recommendation(
        predicted_class, confidence
    )
    
    st.markdown(f"""
    <div class="treatment-card">
        <h4>📋 Treatment Plan</h4>
        <p><strong>Urgency Level:</strong> {treatment_info['urgency']}</p>
        <p><strong>Description:</strong> {treatment_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Treatment steps
    st.write("**Recommended Treatment Steps:**")
    for i, step in enumerate(treatment_info['treatment'], 1):
        st.write(f"{i}. {step}")
    
    # Prevention
    if treatment_info['prevention']:
        st.write("**Prevention:**")
        st.write(treatment_info['prevention'])
    
    # Organic treatment options
    st.subheader("🌿 Organic Treatment Options")
    organic_options = recommender.get_organic_treatment_options(predicted_class)
    for option in organic_options:
        st.write(f"• {option}")
    
    # Log prediction to database
    try:
        prediction_id = database.log_prediction(
            image_path=image_path,
            predicted_class=predicted_class,
            confidence=confidence,
            top_3_predictions=top_3_predictions,
            notes="Prediction from web interface"
        )
        st.success(f"✅ Prediction logged to database (ID: {prediction_id})")
    except Exception as e:
        st.warning(f"⚠️ Could not log prediction: {str(e)}")
    
    # User feedback
    st.subheader("💬 Feedback")
    col1, col2 = st.columns(2)
    
    with col1:
        feedback_type = st.selectbox(
            "Was this prediction helpful?",
            ["", "Correct", "Incorrect", "Partially correct", "Uncertain"]
        )
    
    with col2:
        accuracy_rating = st.slider("Rate the accuracy (1-5)", 1, 5, 3)
    
    if st.button("Submit Feedback") and feedback_type:
        try:
            database.add_user_feedback(
                prediction_id=prediction_id,
                feedback_type=feedback_type,
                accuracy_rating=accuracy_rating
            )
            st.success("✅ Thank you for your feedback!")
        except Exception as e:
            st.error(f"Error submitting feedback: {str(e)}")

def analytics_dashboard(database):
    """Analytics dashboard page"""
    
    st.header("📊 Analytics Dashboard")
    
    # Get statistics
    stats = database.get_disease_statistics()
    accuracy_metrics = database.get_accuracy_metrics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", stats['total_predictions'])
    
    with col2:
        st.metric("Average Confidence", f"{stats['average_confidence']:.2%}")
    
    with col3:
        avg_rating = accuracy_metrics.get('average_rating', 0)
        st.metric("Average Rating", f"{avg_rating:.1f}/5")
    
    with col4:
        feedback_count = sum(accuracy_metrics.get('feedback_distribution', {}).values())
        st.metric("Feedback Count", feedback_count)
    
    # Disease distribution
    if stats['disease_distribution']:
        st.subheader("🌱 Disease Distribution")
        
        disease_data = []
        for disease, count, avg_conf in stats['disease_distribution']:
            disease_data.append({
                'Disease': disease.replace('_', ' ').title(),
                'Count': count,
                'Avg Confidence': f"{avg_conf:.2%}"
            })
        
        disease_df = pd.DataFrame(disease_data)
        st.dataframe(disease_df, use_container_width=True)
        
        # Pie chart
        fig = px.pie(
            disease_df.head(10), 
            values='Count', 
            names='Disease',
            title="Top 10 Most Detected Diseases"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent predictions
    st.subheader("📈 Recent Predictions")
    recent_predictions = database.get_predictions(limit=20)
    
    if not recent_predictions.empty:
        # Convert timestamp to datetime
        recent_predictions['timestamp'] = pd.to_datetime(recent_predictions['timestamp'])
        
        # Time series chart
        daily_counts = recent_predictions.groupby(recent_predictions['timestamp'].dt.date).size()
        
        fig = px.line(
            x=daily_counts.index,
            y=daily_counts.values,
            title="Daily Prediction Count",
            labels={'x': 'Date', 'y': 'Number of Predictions'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent predictions table
        st.write("**Recent Predictions:**")
        display_df = recent_predictions[['timestamp', 'predicted_class', 'confidence']].copy()
        display_df['predicted_class'] = display_df['predicted_class'].str.replace('_', ' ').str.title()
        # Robust formatting: handle bytes/decimal/str -> float
        def _fmt_conf(v):
            try:
                if isinstance(v, (bytes, bytearray)):
                    try:
                        v = v.decode('utf-8', errors='ignore')
                    except Exception:
                        return "0.00%"
                return f"{float(v):.2%}"
            except Exception:
                return "0.00%"
        display_df['confidence'] = display_df['confidence'].apply(_fmt_conf)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No predictions found in the database.")

def treatment_guide_page(recommender):
    """Treatment guide page"""
    
    st.header("🌿 Plant Disease Treatment Guide")
    
    # Disease selection
    st.subheader("🔍 Select a Disease")
    disease_options = list(DISEASE_CLASSES.values())
    selected_disease = st.selectbox("Choose a disease:", [""] + disease_options)
    
    if selected_disease:
        # Get treatment information
        treatment_info = recommender.get_treatment_recommendation(selected_disease)
        
        # Display treatment information
        st.markdown(f"""
        <div class="treatment-card">
            <h3>📋 Treatment Information for {selected_disease.replace('_', ' ').title()}</h3>
            <p><strong>Description:</strong> {treatment_info['description']}</p>
            <p><strong>Urgency Level:</strong> {treatment_info['urgency']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Treatment steps
        st.subheader("💊 Treatment Steps")
        for i, step in enumerate(treatment_info['treatment'], 1):
            st.write(f"{i}. {step}")
        
        # Prevention
        if treatment_info['prevention']:
            st.subheader("🛡️ Prevention")
            st.write(treatment_info['prevention'])
        
        # Organic and chemical options
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌿 Organic Treatments")
            organic_options = recommender.get_organic_treatment_options(selected_disease)
            for option in organic_options:
                st.write(f"• {option}")
        
        with col2:
            st.subheader("🧪 Chemical Treatments")
            chemical_options = recommender.get_chemical_treatment_options(selected_disease)
            for option in chemical_options:
                st.write(f"• {option}")
    
    # General plant care tips
    st.subheader("🌱 General Plant Care Tips")
    care_tips = recommender.get_general_plant_care_tips()
    
    for category, tips in care_tips.items():
        with st.expander(f"📌 {category}"):
            for tip in tips:
                st.write(f"• {tip}")
    
    # Seasonal advice
    st.subheader("📅 Seasonal Care Advice")
    season = st.selectbox("Select Season:", ["Spring", "Summer", "Fall", "Winter"])
    
    if season:
        seasonal_tips = recommender.get_seasonal_advice(season)
        if seasonal_tips:
            for tip in seasonal_tips:
                st.write(f"• {tip}")

def database_management_page(database):
    """Database management page"""
    
    st.header("📝 Database Management")
    
    # Database statistics
    st.subheader("📊 Database Statistics")
    stats = database.get_disease_statistics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Predictions", stats['total_predictions'])
        st.metric("Average Confidence", f"{stats['average_confidence']:.2%}")
    
    with col2:
        st.metric("Unique Diseases", len(stats['disease_distribution']))
        st.metric("Most Common Disease", 
                 stats['disease_distribution'][0][0].replace('_', ' ').title() 
                 if stats['disease_distribution'] else "N/A")
    
    # Export data
    st.subheader("📤 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export to CSV"):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                    database.export_data(tmp_file.name, 'csv')
                    with open(tmp_file.name, 'rb') as f:
                        st.download_button(
                            label="Download CSV",
                            data=f.read(),
                            file_name=f"plant_disease_predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                os.unlink(tmp_file.name)
            except Exception as e:
                st.error(f"Error exporting data: {str(e)}")
    
    with col2:
        if st.button("Export to Excel"):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    database.export_data(tmp_file.name, 'excel')
                    with open(tmp_file.name, 'rb') as f:
                        st.download_button(
                            label="Download Excel",
                            data=f.read(),
                            file_name=f"plant_disease_predictions_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                os.unlink(tmp_file.name)
            except Exception as e:
                st.error(f"Error exporting data: {str(e)}")
    
    # Data cleanup
    st.subheader("🧹 Data Cleanup")
    st.warning("⚠️ This will permanently delete old data!")
    
    days_old = st.slider("Delete data older than (days):", 30, 365, 90)
    
    if st.button("Clean Old Data", type="secondary"):
        try:
            database.cleanup_old_data(days_old)
            st.success("✅ Old data cleaned successfully!")
        except Exception as e:
            st.error(f"Error cleaning data: {str(e)}")

if __name__ == "__main__":
    main()
