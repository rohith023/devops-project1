"""
Flask Web Application for Cloud-Native Drug Recommendation System
Provides REST API endpoints for drug prediction using ML model
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}, r"/*": {"origins": "*"}})

# Load model and encoders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')


def load_model():
    """Load the trained model and encoders"""
    if not os.path.exists(MODEL_PATH):
        print(f"WARNING: Model file not found at {MODEL_PATH}")
        return None
    try:
        print(f"Loading model from {MODEL_PATH} using numpy {numpy.__version__}")
        model_data = joblib.load(MODEL_PATH)
        required_keys = {'model', 'le_bp', 'le_chol', 'le_disease', 'le_drug'}
        missing_keys = required_keys - set(model_data.keys())
        if missing_keys:
            print(f"Error loading model from {MODEL_PATH}: missing keys {sorted(missing_keys)}")
            return None
        return model_data
    except Exception as e:
        print(f"Error loading model from {MODEL_PATH}: {e}")
        return None

# Load model on startup
model_data = load_model()
print(f"DEBUG: Model loaded with keys: {model_data.keys() if model_data else 'None'}")
if model_data and 'le_disease' in model_data:
    print(f"DEBUG: Disease encoder found with classes: {model_data['le_disease'].classes_}")

@app.route('/', methods=['GET'])
def home():
    """Home route - confirms app is running"""
    return jsonify({
        'status': 'success',
        'message': 'Cloud-Native Drug Recommendation System is running',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/predict-form', methods=['GET'])
def predict_form():
    """Serve an HTML form for testing predictions"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Drug Recommendation System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 500px;
                width: 100%;
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 28px;
                margin-bottom: 8px;
                font-weight: 700;
            }
            
            .header p {
                font-size: 14px;
                opacity: 0.9;
            }
            
            .content {
                padding: 40px 30px;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: 600;
                color: #333;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            input[type="number"],
            select {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 14px;
                font-family: inherit;
                transition: all 0.3s ease;
                background: white;
                color: #333;
            }
            
            input[type="number"]:focus,
            select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            select {
                cursor: pointer;
                appearance: none;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23667eea' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
                background-repeat: no-repeat;
                background-position: right 12px center;
                padding-right: 40px;
            }
            
            option {
                padding: 8px;
                color: #333;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                margin-top: 30px;
            }
            
            button {
                flex: 1;
                padding: 14px 24px;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .btn-submit {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn-submit:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
            }
            
            .btn-reset {
                background: #f0f0f0;
                color: #333;
                border: 2px solid #ddd;
            }
            
            .btn-reset:hover {
                background: #e8e8e8;
                border-color: #999;
            }
            
            .result {
                margin-top: 30px;
                padding: 20px;
                border-radius: 10px;
                display: none;
                animation: slideIn 0.3s ease;
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .result.success {
                background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
                border: 2px solid #56ab91;
            }
            
            .result.error {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                border: 2px solid #e74c3c;
            }
            
            .result-title {
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 15px;
                color: #333;
                display: flex;
                align-items: center;
            }
            
            .result-icon {
                font-size: 24px;
                margin-right: 10px;
            }
            
            .result-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
            }
            
            .result-item {
                background: rgba(255, 255, 255, 0.8);
                padding: 12px;
                border-radius: 8px;
            }
            
            .result-label {
                font-size: 12px;
                font-weight: 600;
                color: #666;
                text-transform: uppercase;
                margin-bottom: 4px;
            }
            
            .result-value {
                font-size: 16px;
                font-weight: 700;
                color: #333;
            }
            
            .confidence-bar {
                background: rgba(255, 255, 255, 0.5);
                border-radius: 6px;
                height: 8px;
                margin-top: 4px;
                overflow: hidden;
            }
            
            .confidence-fill {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                height: 100%;
                border-radius: 6px;
                transition: width 0.5s ease;
            }
            
            .error-message {
                color: #c0392b;
                font-weight: 600;
            }
            
            .info-box {
                background: #f8f9ff;
                border-left: 4px solid #667eea;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-size: 13px;
                color: #555;
                line-height: 1.5;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            
            .spinner {
                border: 3px solid #f0f0f0;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .stats {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            
            .stat-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 12px;
            }
            
            .stat-value {
                font-size: 18px;
                font-weight: 700;
            }
            
            .stat-label {
                font-size: 11px;
                opacity: 0.9;
                margin-top: 4px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Rx Predictor</h1>
                <p>AI-Powered Drug Recommendation System</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-value">97.78%</div>
                        <div class="stat-label">Accuracy</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">5</div>
                        <div class="stat-label">Drugs</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">4</div>
                        <div class="stat-label">Diseases</div>
                    </div>
                </div>
                
                <div class="info-box">
                    Enter patient information to receive AI-powered drug recommendations based on medical parameters.
                </div>
                
                <form id="predictForm">
                    <div class="form-group">
                        <label for="age">Patient Age</label>
                        <input type="number" id="age" name="age" required min="0" max="150" value="45" placeholder="e.g., 45">
                    </div>
                    
                    <div class="form-group">
                        <label for="bp">Blood Pressure</label>
                        <select id="bp" name="bp" required>
                            <option value="">Select blood pressure level...</option>
                            <option value="LOW">LOW</option>
                            <option value="NORMAL" selected>NORMAL</option>
                            <option value="HIGH">HIGH</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="cholesterol">Cholesterol Level</label>
                        <select id="cholesterol" name="cholesterol" required>
                            <option value="">Select cholesterol level...</option>
                            <option value="NORMAL" selected>NORMAL</option>
                            <option value="HIGH">HIGH</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="disease">Primary Disease</label>
                        <select id="disease" name="disease" required>
                            <option value="">Select disease...</option>
                            <option value="Hypertension">Hypertension</option>
                            <option value="Diabetes">Diabetes</option>
                            <option value="Fever">Fever</option>
                            <option value="Allergy">Allergy</option>
                        </select>
                    </div>
                    
                    <div class="button-group">
                        <button type="submit" class="btn-submit">Get Recommendation</button>
                        <button type="reset" class="btn-reset">Clear</button>
                    </div>
                </form>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing patient data...</p>
                </div>
                
                <div class="result" id="result"></div>
            </div>
        </div>
        
        <script>
            document.getElementById('predictForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const data = {
                    age: parseFloat(document.getElementById('age').value),
                    bp: document.getElementById('bp').value,
                    cholesterol: document.getElementById('cholesterol').value,
                    disease: document.getElementById('disease').value
                };
                
                const loading = document.getElementById('loading');
                const resultDiv = document.getElementById('result');
                
                loading.style.display = 'block';
                resultDiv.style.display = 'none';
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    loading.style.display = 'none';
                    
                    if (response.ok) {
                        const pred = result.prediction;
                        const confidence = Math.round(pred.confidence * 100);
                        
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = `
                            <div class="result-title">
                                <span class="result-icon">💊</span>
                                Recommended Drug
                            </div>
                            <div class="result-content">
                                <div class="result-item">
                                    <div class="result-label">Drug Name</div>
                                    <div class="result-value">${pred.drug}</div>
                                </div>
                                <div class="result-item">
                                    <div class="result-label">Confidence</div>
                                    <div class="result-value">${confidence}%</div>
                                    <div class="confidence-bar">
                                        <div class="confidence-fill" style="width: ${confidence}%"></div>
                                    </div>
                                </div>
                                <div class="result-item">
                                    <div class="result-label">Patient Age</div>
                                    <div class="result-value">${data.age}</div>
                                </div>
                                <div class="result-item">
                                    <div class="result-label">Disease</div>
                                    <div class="result-value">${data.disease}</div>
                                </div>
                            </div>
                        `;
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = `
                            <div class="result-title">
                                <span class="result-icon">⚠️</span>
                                Error
                            </div>
                            <p class="error-message">${result.message}</p>
                        `;
                    }
                    resultDiv.style.display = 'block';
                } catch (error) {
                    loading.style.display = 'none';
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `
                        <div class="result-title">
                            <span class="result-icon">❌</span>
                            Connection Error
                        </div>
                        <p class="error-message">${error.message}</p>
                    `;
                    resultDiv.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_status = "loaded" if model_data is not None else "not_loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/test-disease', methods=['GET'])
def test_disease():
    """Test endpoint for disease feature"""
    return jsonify({
        'test': 'disease endpoint',
        'message': 'This is a fresh endpoint to test if Flask reloads'
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict drug recommendation based on patient features
    
    Expected JSON input:
    {
        "age": 45,
        "bp": "HIGH",
        "cholesterol": "NORMAL",
        "disease": "Hypertension"
    }
    
    Valid BP values: LOW, NORMAL, HIGH
    Valid Cholesterol values: LOW, NORMAL, HIGH
    Valid Disease values: Hypertension, Diabetes, Fever, Allergy
    """
    try:
        print(f"DEBUG: predict() called")
        # Check if model is loaded
        if model_data is None:
            return jsonify({
                'status': 'error',
                'message': 'Model not loaded. Please train the model first.',
                'timestamp': datetime.utcnow().isoformat()
            }), 503
        
        # Get JSON data
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        required_fields = ['age', 'bp', 'cholesterol', 'disease']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        
        age = data['age']
        bp = data['bp']
        cholesterol = data['cholesterol']
        disease = data['disease']
        print(f"DEBUG: Extracted - age={age}, bp={bp}, chol={cholesterol}, disease={disease}")
        
        # Validate age
        try:
            age = float(age)
            if age < 0 or age > 150:
                raise ValueError("Age must be between 0 and 150")
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Age must be a valid number between 0 and 150',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Validate BP and Cholesterol
        valid_bp = ['LOW', 'NORMAL', 'HIGH']
        valid_chol = ['LOW', 'NORMAL', 'HIGH']
        valid_diseases = ['Hypertension', 'Diabetes', 'Fever', 'Allergy']
        
        bp_upper = bp.upper()
        chol_upper = cholesterol.upper()
        
        if bp_upper not in valid_bp:
            return jsonify({
                'status': 'error',
                'message': f'BP must be one of: {", ".join(valid_bp)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if chol_upper not in valid_chol:
            return jsonify({
                'status': 'error',
                'message': f'Cholesterol must be one of: {", ".join(valid_chol)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if disease not in valid_diseases:
            return jsonify({
                'status': 'error',
                'message': f'Disease must be one of: {", ".join(valid_diseases)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Encode features
        bp_encoded = model_data['le_bp'].transform([bp_upper])[0]
        chol_encoded = model_data['le_chol'].transform([chol_upper])[0]
        disease_encoded = model_data['le_disease'].transform([disease])[0]
        
        # Make prediction
        features = np.array([[age, bp_encoded, chol_encoded, disease_encoded]])
        prediction = model_data['model'].predict(features)[0]
        
        # Decode prediction
        predicted_drug = model_data['le_drug'].inverse_transform([prediction])[0]
        
        # Get prediction confidence
        probabilities = model_data['model'].predict_proba(features)[0]
        confidence = float(np.max(probabilities))
        
        return jsonify({
            'status': 'success',
            'prediction': {
                'drug': predicted_drug,
                'confidence': round(confidence, 4)
            },
            'input': {
                'age': age,
                'bp': bp_upper,
                'cholesterol': chol_upper,
                'disease': disease
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        import traceback
        print(f"DEBUG EXCEPTION in predict: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Prediction error: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    if model_data is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded',
            'timestamp': datetime.utcnow().isoformat()
        }), 503
    
    model = model_data['model']
    return jsonify({
        'status': 'success',
        'model_info': {
            'type': 'DecisionTreeClassifier',
            'max_depth': int(model.max_depth),
            'n_leaves': int(model.get_n_leaves()),
            'n_features': int(model.n_features_in_)
        },
        'features': ['Age', 'BP', 'Cholesterol', 'Disease'],
        'feature_values': {
            'bp': model_data['le_bp'].classes_.tolist(),
            'cholesterol': model_data['le_chol'].classes_.tolist(),
            'disease': model_data['le_disease'].classes_.tolist()
        },
        'drugs': model_data['le_drug'].classes_.tolist(),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'timestamp': datetime.utcnow().isoformat()
    }), 500

if __name__ == '__main__':
    if model_data is None:
        print("WARNING: Model not found. Please train the model using: python train/train_model.py")
        print("The app will run but predictions will fail until the model is trained.")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
