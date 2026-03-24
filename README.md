# 🌱 Plant Disease Detection System

An intelligent system that automatically detects and classifies plant leaf diseases using deep learning techniques (ResNet50). The system processes input images, identifies disease types, and provides treatment recommendations with confidence scores.

## 🚀 Features

- **Deep Learning Model**: Uses ResNet50 with transfer learning for accurate disease classification
- **Web Interface**: User-friendly Streamlit web application for image upload and analysis
- **Treatment Recommendations**: Provides detailed treatment suggestions for detected diseases
- **Database Logging**: SQLite database for storing predictions and user feedback
- **Analytics Dashboard**: Comprehensive analytics and visualization of prediction data
- **Organic & Chemical Treatments**: Both organic and chemical treatment options
- **Confidence Scoring**: Shows prediction confidence and top-3 alternatives

## 📋 System Requirements

- Python 3.8 or higher
- TensorFlow 2.15.0
- Streamlit 1.28.1
- OpenCV 4.8.1
- Other dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd plant-disease-detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create necessary directories**
   ```bash
   mkdir data models uploads
   ```

## 🏃‍♂️ Quick Start

### 1. Run the Web Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 2. Upload and Analyze Images

1. Go to the "Home - Disease Detection" page
2. Upload an image of a plant leaf (JPG, PNG)
3. Click "Analyze Image" to get predictions
4. View disease classification, confidence scores, and treatment recommendations

## 📊 Dataset Information

The system is designed to work with the PlantVillage dataset, which includes:

- **38 disease classes** covering various plant diseases
- **Healthy and diseased** leaf images
- **Multiple plant types**: Apple, Tomato, Potato, Grape, Corn, etc.

### Sample Classes:
- Apple___Apple_scab
- Apple___Black_rot
- Tomato___Early_blight
- Tomato___Late_blight
- Potato___Late_blight
- Grape___Black_rot
- And many more...

## 🏗️ Project Structure

```
plant-disease-detection/
├── app.py                      # Main Streamlit application
├── model.py                    # ResNet50 model implementation
├── data_preprocessing.py       # Image preprocessing utilities
├── database.py                 # SQLite database operations
├── treatment_recommender.py    # Treatment recommendation system
├── config.py                   # Configuration settings
├── train_model.py             # Model training script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── data/                      # Dataset directory
├── models/                    # Trained model files
└── uploads/                   # Temporary upload directory
```

## 🎯 Model Training

### Training with Your Own Dataset

1. **Prepare your dataset** in the following structure:
   ```
   data/
   ├── PlantVillage/
   │   ├── Apple___Apple_scab/
   │   ├── Apple___Black_rot/
   │   ├── Tomato___Early_blight/
   │   └── ...
   ```

2. **Run the training script**:
   ```bash
   python train_model.py --data_dir data/PlantVillage --epochs 50
   ```

3. **Training options**:
   ```bash
   python train_model.py --help
   ```

### Training Parameters

- `--data_dir`: Path to dataset directory
- `--epochs`: Number of training epochs (default: 50)
- `--batch_size`: Batch size for training (default: 32)
- `--fine_tune`: Enable fine-tuning after initial training

## 🔧 Configuration

Edit `config.py` to customize:

- **Model parameters**: Input size, number of classes, learning rate
- **Data settings**: Train/validation splits, augmentation
- **Disease classes**: Add or modify disease classifications
- **Treatment recommendations**: Customize treatment suggestions

## 📱 Web Interface Features

### 1. Disease Detection Page
- Upload plant leaf images
- View prediction results with confidence scores
- See top-3 alternative predictions
- Get treatment recommendations
- Provide feedback on predictions

### 2. Analytics Dashboard
- View prediction statistics
- Disease distribution charts
- Daily prediction trends
- User feedback metrics

### 3. Treatment Guide
- Browse treatment information by disease
- Organic and chemical treatment options
- General plant care tips
- Seasonal care advice

### 4. Database Management
- Export prediction data
- View database statistics
- Clean up old data
- Download reports

## 🗄️ Database Schema

The system uses SQLite with the following tables:

- **predictions**: Stores prediction results and metadata
- **disease_info**: Disease descriptions and treatment information
- **user_feedback**: User feedback on prediction accuracy

## 🌿 Treatment Recommendations

The system provides comprehensive treatment information:

- **Disease descriptions**
- **Step-by-step treatment plans**
- **Organic treatment options**
- **Chemical treatment options**
- **Prevention strategies**
- **Urgency levels**

## 📈 Performance Metrics

The model provides several accuracy metrics:

- **Top-1 Accuracy**: Primary prediction accuracy
- **Top-3 Accuracy**: Accuracy within top 3 predictions
- **Confidence Scores**: Prediction confidence levels
- **User Feedback**: Real-world accuracy validation

## 🔍 API Usage

### Using the Model Programmatically

```python
from model import PlantDiseaseModel
from data_preprocessing import DataPreprocessor

# Load model
model = PlantDiseaseModel()
model.load_model('models/plant_disease_model.h5')

# Preprocess image
preprocessor = DataPreprocessor()
processed_image = preprocessor.preprocess_image('path/to/image.jpg')

# Make prediction
predicted_class, confidence, top_3 = model.predict(processed_image)
print(f"Predicted: {predicted_class} (Confidence: {confidence:.2%})")
```

## 🚨 Troubleshooting

### Common Issues

1. **Model not found error**
   - Run `python train_model.py` to create a sample model
   - Or download a pre-trained model

2. **Memory issues during training**
   - Reduce batch size: `--batch_size 16`
   - Use smaller input images

3. **Poor prediction accuracy**
   - Ensure good quality input images
   - Check if the disease is in the training dataset
   - Consider retraining with more data

4. **Streamlit app not loading**
   - Check if all dependencies are installed
   - Verify Python version compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **PlantVillage Dataset**: For providing the comprehensive plant disease dataset
- **TensorFlow/Keras**: For the deep learning framework
- **Streamlit**: For the web interface framework
- **ResNet50**: For the pre-trained model architecture

## 📞 Support

For questions, issues, or contributions:

1. Check the troubleshooting section
2. Review the code documentation
3. Open an issue on the repository
4. Contact the development team

## 🔮 Future Enhancements

- [ ] Mobile app development
- [ ] Real-time camera integration
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Integration with IoT sensors
- [ ] Cloud deployment options
- [ ] API endpoints for external integration

---

**Happy Plant Disease Detection! 🌱🔬**
