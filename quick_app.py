"""
Quick Flask web interface for Plant Disease Detection
Minimal dependencies - works while training runs
"""

from flask import Flask, render_template, request, jsonify
import os
import numpy as np
from PIL import Image
import io
import base64
import json
from pathlib import Path

app = Flask(__name__)

# Configuration
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'plant_disease_model.h5')

class SimplePredictor:
    """Simple predictor that works without full model"""
    
    def __init__(self):
        self.class_indices = None
        self.load_class_indices()
    
    def load_class_indices(self):
        """Load class indices from saved JSON"""
        class_indices_path = os.path.join(MODEL_DIR, 'class_indices.json')
        if os.path.exists(class_indices_path):
            with open(class_indices_path, 'r') as f:
                data = json.load(f)
                self.class_indices = {v: k for k, v in data.items()}
    
    def predict(self, image_array):
        """Placeholder prediction - will work once model is trained"""
        if not os.path.exists(MODEL_PATH):
            return {
                'status': 'model_training',
                'message': 'Model is currently training. Please check back in 1-3 hours.',
                'classes': list(self.class_indices.values()) if self.class_indices else []
            }
        
        try:
            from keras.models import load_model
            model = load_model(MODEL_PATH)
            predictions = model.predict(image_array, verbose=0)
            predicted_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_idx])
            
            if self.class_indices and predicted_idx in self.class_indices:
                predicted_class = self.class_indices[predicted_idx]
            else:
                predicted_class = f"Class_{predicted_idx}"
            
            return {
                'status': 'success',
                'prediction': predicted_class,
                'confidence': confidence,
                'all_predictions': predictions[0].tolist()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

predictor = SimplePredictor()

@app.route('/')
def index():
    """Home page"""
    model_exists = os.path.exists(MODEL_PATH)
    class_count = len(predictor.class_indices) if predictor.class_indices else 0
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plant Disease Detection System</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            header {{ background: white; border-radius: 10px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            h1 {{ color: #333; margin-bottom: 10px; }}
            .status {{ padding: 15px; border-radius: 5px; margin-top: 15px; }}
            .status.training {{ background: #fff3cd; color: #856404; }}
            .status.ready {{ background: #d4edda; color: #155724; }}
            .content {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .card {{ background: white; border-radius: 10px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            .card h2 {{ color: #667eea; margin-bottom: 15px; }}
            .upload-area {{ border: 2px dashed #667eea; border-radius: 5px; padding: 30px; text-align: center; cursor: pointer; transition: all 0.3s; }}
            .upload-area:hover {{ background: #f0f4ff; }}
            input[type="file"] {{ display: none; }}
            button {{ background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background: #764ba2; }}
            .info {{ background: #f0f4ff; padding: 15px; border-radius: 5px; margin-top: 10px; }}
            .info p {{ margin: 5px 0; color: #555; }}
            footer {{ text-align: center; color: white; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🌱 Plant Disease Detection System</h1>
                <div class="status {'ready' if model_exists else 'training'}">
                    <strong>{'✅ Model Ready!' if model_exists else '⏳ Model Training'}</strong>
                    <p>{'Upload an image to detect plant diseases.' if model_exists else 'Training in progress. Current status: See terminal. Check back soon!'}</p>
                </div>
                {f'<p style="margin-top: 10px; color: #666;">Classes detected: {class_count}</p>' if class_count > 0 else ''}
            </header>
            
            <div class="content">
                <div class="card">
                    <h2>📸 Upload Image</h2>
                    <div class="upload-area" onclick="document.getElementById('file-input').click()">
                        <p>Click to upload or drag and drop</p>
                        <p style="font-size: 12px; color: #999; margin-top: 5px;">JPG, PNG up to 10MB</p>
                    </div>
                    <input type="file" id="file-input" accept="image/*">
                    <button onclick="uploadImage()" style="width: 100%; margin-top: 15px;">Analyze Image</button>
                </div>
                
                <div class="card">
                    <h2>📊 System Info</h2>
                    <div class="info">
                        <p><strong>Model Status:</strong> {'Ready for predictions' if model_exists else 'Training (check terminal)'}</p>
                        <p><strong>Model Path:</strong> {MODEL_PATH}</p>
                        <p><strong>Classes:</strong> {class_count} disease types</p>
                        <p><strong>Training Data:</strong> data/PlantVillage</p>
                    </div>
                    <p style="margin-top: 15px; color: #666; font-size: 14px;">
                        <strong>Next Steps:</strong><br>
                        1. Monitor training progress in terminal<br>
                        2. Once complete, refresh this page<br>
                        3. Upload a plant leaf image to detect diseases
                    </p>
                </div>
            </div>
            
            <footer>
                <p>Plant Disease Detection System © 2025 | Training in progress...</p>
            </footer>
        </div>
        
        <script>
            function uploadImage() {{
                const fileInput = document.getElementById('file-input');
                const file = fileInput.files[0];
                
                if (!file) {{
                    alert('Please select an image');
                    return;
                }}
                
                const formData = new FormData();
                formData.append('image', file);
                
                fetch('/predict', {{
                    method: 'POST',
                    body: formData
                }})
                .then(r => r.json())
                .then(data => {{
                    if (data.status === 'model_training') {{
                        alert('Model is still training. Please wait and try again later.');
                    }} else if (data.status === 'success') {{
                        alert(`Prediction: ${{data.prediction}}\\nConfidence: ${{(data.confidence * 100).toFixed(2)}}%`);
                    }} else {{
                        alert(`Error: ${{data.message}}`);
                    }}
                }})
                .catch(e => alert('Upload failed: ' + e));
            }}
            
            document.getElementById('file-input').addEventListener('change', function(e) {{
                const file = e.target.files[0];
                if (file) {{
                    console.log('Selected:', file.name);
                }}
            }});
        </script>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction on uploaded image"""
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image provided'})
    
    try:
        image = Image.open(request.files['image'].stream)
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        result = predictor.predict(image_array)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/status')
def status():
    """Check training status"""
    model_exists = os.path.exists(MODEL_PATH)
    return jsonify({
        'model_ready': model_exists,
        'model_path': MODEL_PATH,
        'classes': len(predictor.class_indices) if predictor.class_indices else 0
    })

if __name__ == '__main__':
    print("🚀 Starting Flask web server on http://localhost:5000")
    print("📌 Training is running in parallel. Refresh page when model is ready.")
    app.run(debug=False, host='localhost', port=5000)
