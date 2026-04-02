"""
Flask Web Application for Cloud-Native Drug Recommendation System
Provides REST API endpoints for drug prediction using ML model
"""
from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import sys
from datetime import datetime

app = Flask(__name__)

# Load model and encoders
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')

def load_model():
    """Load the trained model and encoders"""
    if not os.path.exists(model_path):
        return None, None, None, None
    model_data = joblib.load(model_path)
    return (
        model_data['model'],
        model_data['le_bp'],
        model_data['le_chol'],
        model_data['le_drug']
    )

# Load model on startup
model, le_bp, le_chol, le_drug = load_model()

@app.route('/', methods=['GET'])
def home():
    """Home route - confirms app is running"""
    return jsonify({
        'status': 'success',
        'message': 'Cloud-Native Drug Recommendation System is running',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not_loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict drug recommendation based on patient features
    
    Expected JSON input:
    {
        "age": 45,
        "bp": "HIGH",
        "cholesterol": "NORMAL"
    }
    
    Valid BP values: LOW, NORMAL, HIGH
    Valid Cholesterol values: LOW, NORMAL, HIGH
    """
    try:
        # Check if model is loaded
        if model is None:
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
        
        required_fields = ['age', 'bp', 'cholesterol']
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
        valid_values = ['LOW', 'NORMAL', 'HIGH']
        bp_upper = bp.upper()
        chol_upper = cholesterol.upper()
        
        if bp_upper not in valid_values:
            return jsonify({
                'status': 'error',
                'message': f'BP must be one of: {", ".join(valid_values)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if chol_upper not in valid_values:
            return jsonify({
                'status': 'error',
                'message': f'Cholesterol must be one of: {", ".join(valid_values)}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Encode features
        bp_encoded = le_bp.transform([bp_upper])[0]
        chol_encoded = le_chol.transform([chol_upper])[0]
        
        # Make prediction
        features = np.array([[age, bp_encoded, chol_encoded]])
        prediction = model.predict(features)[0]
        
        # Decode prediction
        predicted_drug = le_drug.inverse_transform([prediction])[0]
        
        # Get prediction confidence
        probabilities = model.predict_proba(features)[0]
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
                'cholesterol': chol_upper
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Prediction error: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    if model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded',
            'timestamp': datetime.utcnow().isoformat()
        }), 503
    
    return jsonify({
        'status': 'success',
        'model_info': {
            'type': 'DecisionTreeClassifier',
            'max_depth': model.max_depth,
            'n_leaves': model.get_n_leaves(),
            'n_features': model.n_features_in_
        },
        'features': ['Age', 'BP', 'Cholesterol'],
        'drugs': le_drug.classes_.tolist(),
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
    if model is None:
        print("WARNING: Model not found. Please train the model using: python train/train_model.py")
        print("The app will run but predictions will fail until the model is trained.")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
