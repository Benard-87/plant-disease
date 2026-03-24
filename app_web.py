"""
Lightweight web app using Flask + HTML for Plant Disease Detection
Works with your MySQL database (root / 1234)
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import numpy as np
from PIL import Image
import io
import base64
from pathlib import Path
from datetime import datetime

# Database imports
from database import PlantDiseaseDB
from treatment_recommender import TreatmentRecommender

app = Flask(__name__)

# Configuration
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'plant_disease_model.h5')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database and recommender
db = PlantDiseaseDB()
recommender = TreatmentRecommender()

class ModelPredictor:
    """Handle model predictions"""
    
    def __init__(self):
        self.model = None
        self.class_indices = None
        self.load_model()
    
    def load_model(self):
        """Load trained model if available"""
        if not os.path.exists(MODEL_PATH):
            return False
        
        try:
            from keras.models import load_model
            self.model = load_model(MODEL_PATH)
            
            # Load class indices
            indices_path = os.path.join(MODEL_DIR, 'class_indices.json')
            if os.path.exists(indices_path):
                with open(indices_path, 'r') as f:
                    data = json.load(f)
                    self.class_indices = {int(v): k for k, v in data.items()}
            
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, image_array):
        """Make prediction on image"""
        if self.model is None:
            return None
        
        try:
            predictions = self.model.predict(image_array, verbose=0)
            predicted_idx = int(np.argmax(predictions[0]))
            confidence = float(predictions[0][predicted_idx])
            
            # Get class name
            if self.class_indices and predicted_idx in self.class_indices:
                predicted_class = self.class_indices[predicted_idx]
            else:
                predicted_class = f"Class_{predicted_idx}"
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            top_3 = []
            for idx in top_3_indices:
                if self.class_indices and idx in self.class_indices:
                    class_name = self.class_indices[idx]
                else:
                    class_name = f"Class_{idx}"
                conf = float(predictions[0][idx])
                top_3.append((class_name, conf))
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'top_3': top_3
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

predictor = ModelPredictor()

@app.route('/')
def index():
    """Main page"""
    model_ready = predictor.model is not None
    status = "✅ Ready for predictions" if model_ready else "⏳ Model training..."
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Plant Disease Detection System</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            header {{ 
                background: white; 
                border-radius: 15px; 
                padding: 40px; 
                margin-bottom: 30px; 
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
            }}
            h1 {{ color: #333; margin-bottom: 15px; font-size: 2.5em; }}
            .status {{ 
                padding: 15px 25px; 
                border-radius: 8px; 
                display: inline-block;
                font-weight: bold;
                font-size: 1.1em;
                background: {'#d4edda' if model_ready else '#fff3cd'};
                color: {'#155724' if model_ready else '#856404'};
            }}
            .content {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
            .card {{ 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            .card h2 {{ color: #667eea; margin-bottom: 20px; font-size: 1.5em; }}
            .upload-area {{ 
                border: 2px dashed #667eea; 
                border-radius: 10px; 
                padding: 40px; 
                text-align: center; 
                cursor: pointer;
                transition: all 0.3s;
            }}
            .upload-area:hover {{ background: #f0f4ff; border-color: #764ba2; }}
            input[type="file"] {{ display: none; }}
            button {{ 
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white; 
                border: none; 
                padding: 12px 30px; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
                width: 100%;
                transition: all 0.3s;
            }}
            button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3); }}
            button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .result {{ 
                background: #f0f4ff; 
                padding: 20px; 
                border-radius: 10px; 
                margin-top: 20px;
                border-left: 4px solid #667eea;
            }}
            .result h3 {{ color: #333; margin-bottom: 10px; }}
            .result p {{ color: #555; margin-bottom: 8px; }}
            .confidence {{ font-size: 1.3em; font-weight: bold; color: #667eea; }}
            .top-3 {{ margin-top: 15px; }}
            .top-3 li {{ margin: 5px 0; color: #666; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }}
            .info-item {{ background: #f0f4ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; }}
            .info-item strong {{ color: #333; }}
            footer {{ text-align: center; color: white; margin-top: 40px; }}
            .loading {{ display: none; text-align: center; margin-top: 20px; }}
            .spinner {{ 
                border: 4px solid #f0f4ff; 
                border-top: 4px solid #667eea; 
                border-radius: 50%; 
                width: 40px; 
                height: 40px; 
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }}
            @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
            .treatment {{ background: #e8f5e9; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #28a745; }}
            .treatment h4 {{ color: #1b5e20; margin-bottom: 10px; }}
            .treatment ul {{ margin-left: 20px; color: #2e7d32; }}
            .treatment li {{ margin: 5px 0; }}
            .preview {{ max-width: 300px; margin: 15px auto; }}
            .preview img {{ width: 100%; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🌱 Plant Disease Detection System</h1>
                <p style="color: #666; margin-bottom: 20px;">AI-Powered Plant Health Analysis</p>
                <div class="status">{status}</div>
            </header>
            
            <div class="content">
                <div class="card">
                    <h2>📸 Upload Plant Image</h2>
                    <div class="upload-area" onclick="document.getElementById('file-input').click()">
                        <p style="font-size: 3em; margin-bottom: 10px;">📁</p>
                        <p style="color: #667eea; font-weight: bold;">Click to upload or drag & drop</p>
                        <p style="color: #999; font-size: 0.9em; margin-top: 5px;">JPG, PNG up to 10MB</p>
                    </div>
                    <div class="preview" id="preview" style="display: none;">
                        <img id="preview-img" src="" alt="Preview">
                    </div>
                    <input type="file" id="file-input" accept="image/*">
                    <button onclick="uploadImage()" {'disabled' if not model_ready else ''}>
                        Analyze Image
                    </button>
                    
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <p style="margin-top: 10px; color: white;">Analyzing image...</p>
                    </div>
                    
                    <div id="result"></div>
                </div>
                
                <div class="card">
                    <h2>📊 System Information</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <strong>Model Status:</strong><br>
                            {status}
                        </div>
                        <div class="info-item">
                            <strong>Database:</strong><br>
                            MySQL (plant_disease)
                        </div>
                        <div class="info-item">
                            <strong>Framework:</strong><br>
                            Keras (TensorFlow)
                        </div>
                        <div class="info-item">
                            <strong>Dataset:</strong><br>
                            PlantVillage (50 epochs)
                        </div>
                    </div>
                    
                    <h3 style="margin-top: 25px; margin-bottom: 15px; color: #667eea;">Quick Stats</h3>
                    <div style="background: #f0f4ff; padding: 15px; border-radius: 8px;">
                        <p><strong>Model Path:</strong> models/plant_disease_model.h5</p>
                        <p style="margin-top: 8px;"><strong>Classes:</strong> 37+ disease types</p>
                        <p style="margin-top: 8px;"><strong>Input Size:</strong> 224×224 pixels</p>
                        <p style="margin-top: 8px;"><strong>Predictions Saved:</strong> MySQL DB</p>
                    </div>
                </div>
            </div>
            
            <footer>
                <p>🌿 Plant Disease Detection System © 2025 | Powered by AI & Machine Learning</p>
                <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.9;">Connected to MySQL database | Real-time predictions</p>
            </footer>
        </div>
        
        <script>
            const fileInput = document.getElementById('file-input');
            const preview = document.getElementById('preview');
            const previewImg = document.getElementById('preview-img');
            const resultDiv = document.getElementById('result');
            const loading = document.getElementById('loading');
            
            fileInput.addEventListener('change', function(e) {{
                const file = e.target.files[0];
                if (file) {{
                    const reader = new FileReader();
                    reader.onload = function(event) {{
                        previewImg.src = event.target.result;
                        preview.style.display = 'block';
                    }};
                    reader.readAsDataURL(file);
                }}
            }});
            
            function uploadImage() {{
                const file = fileInput.files[0];
                if (!file) {{
                    alert('Please select an image');
                    return;
                }}
                
                loading.style.display = 'block';
                resultDiv.innerHTML = '';
                
                const formData = new FormData();
                formData.append('image', file);
                
                fetch('/predict', {{
                    method: 'POST',
                    body: formData
                }})
                .then(r => r.json())
                .then(data => {{
                    loading.style.display = 'none';
                    
                    if (data.status === 'success') {{
                        let html = `
                            <div class="result">
                                <h3>🎯 Prediction Result</h3>
                                <p><strong>Disease:</strong> ${{data.predicted_class}}</p>
                                <p class="confidence">Confidence: ${{(data.confidence * 100).toFixed(2)}}%</p>
                                
                                <div class="top-3">
                                    <strong>Top 3 Predictions:</strong>
                                    <ul>
                        `;
                        data.top_3.forEach((pred, i) => {{
                            html += `<li>${{i+1}}. ${{pred[0]}} (${{(pred[1]*100).toFixed(1)}}%)</li>`;
                        }});
                        html += `
                                    </ul>
                                </div>
                        `;
                        
                        if (data.treatment) {{
                            html += `
                                <div class="treatment">
                                    <h4>💊 Treatment Recommendations</h4>
                                    <ul>
                        `;
                            data.treatment.forEach(t => {{
                                html += `<li>${{t}}</li>`;
                            }});
                            html += `
                                    </ul>
                                </div>
                            `;
                        }}
                        
                        html += `</div>`;
                        resultDiv.innerHTML = html;
                    }} else if (data.status === 'model_training') {{
                        resultDiv.innerHTML = `
                            <div class="result" style="background: #fff3cd; border-left-color: #ffc107;">
                                <h3>⏳ Model Training</h3>
                                <p>The model is still training. Please check back later. Training usually takes 1-3 hours.</p>
                            </div>
                        `;
                    }} else {{
                        resultDiv.innerHTML = `<div class="result" style="background: #ffebee; border-left-color: #f44336;">Error: ${{data.message}}</div>`;
                    }}
                }})
                .catch(e => {{
                    loading.style.display = 'none';
                    resultDiv.innerHTML = `<div class="result" style="background: #ffebee; border-left-color: #f44336;">Upload failed: ${{e}}</div>`;
                }});
            }}
        </script>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction"""
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image provided'})
    
    if predictor.model is None:
        return jsonify({'status': 'model_training', 'message': 'Model is training. Please try again later.'})
    
    try:
        image = Image.open(request.files['image'].stream)
        image = image.convert('RGB')
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        result = predictor.predict(image_array)
        
        if result is None:
            return jsonify({'status': 'error', 'message': 'Prediction failed'})
        
        # Get treatment recommendations
        treatment = recommender.get_treatment(result['predicted_class'])
        
        # Save to database
        try:
            db.save_prediction(
                image_path='web_upload',
                predicted_class=result['predicted_class'],
                confidence=result['confidence'],
                top_3_predictions=json.dumps(result['top_3']),
                treatment_applied=json.dumps(treatment['treatment']) if treatment else None
            )
        except:
            pass  # Database optional
        
        return jsonify({
            'status': 'success',
            'predicted_class': result['predicted_class'],
            'confidence': result['confidence'],
            'top_3': result['top_3'],
            'treatment': treatment['treatment'] if treatment else []
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/status')
def status():
    """Check system status"""
    return jsonify({
        'model_ready': predictor.model is not None,
        'model_path': MODEL_PATH,
        'database': 'MySQL (plant_disease)',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Plant Disease Detection Web App")
    print("📍 Open browser to: http://localhost:5000")
    print("💾 Connected to MySQL: root@localhost:plant_disease")
    print("⏸ Press Ctrl+C to stop\n")
    app.run(debug=False, host='localhost', port=5000, threaded=True)
