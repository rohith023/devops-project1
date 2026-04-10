"""
Machine Learning Model Training Script
Trains a Decision Tree Classifier for drug recommendation based on patient features
Features: Age, Blood Pressure, Cholesterol, Disease
"""
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import sys

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(project_root, 'data', 'drug_disease.csv')
model_path = os.path.join(project_root, 'model.pkl')

def train_model():
    """Train the decision tree model with disease feature and save it"""
    print("=" * 60)
    print("DRUG RECOMMENDATION MODEL TRAINING")
    print("=" * 60)
    
    print("\nLoading data from:", data_path)
    
    # Load data
    df = pd.read_csv(data_path)
    print(f"Data shape: {df.shape}")
    print(f"Data columns: {df.columns.tolist()}")
    
    # Display sample data
    print("\nSample data:")
    print(df.head())
    
    # Initialize label encoders for each categorical feature
    le_bp = LabelEncoder()
    le_chol = LabelEncoder()
    le_disease = LabelEncoder()
    le_drug = LabelEncoder()
    
    # Encode categorical features
    print("\nEncoding categorical features...")
    df['BP'] = le_bp.fit_transform(df['BP'])
    df['Cholesterol'] = le_chol.fit_transform(df['Cholesterol'])
    df['Disease'] = le_disease.fit_transform(df['Disease'])
    df['Drug'] = le_drug.fit_transform(df['Drug'])
    
    print("Encoded data mapping:")
    print(f"  BP: {dict(zip(le_bp.classes_, le_bp.transform(le_bp.classes_)))}")
    print(f"  Cholesterol: {dict(zip(le_chol.classes_, le_chol.transform(le_chol.classes_)))}")
    print(f"  Disease: {dict(zip(le_disease.classes_, le_disease.transform(le_disease.classes_)))}")
    print(f"  Drug: {dict(zip(le_drug.classes_, le_drug.transform(le_drug.classes_)))}")
    
    print("\nEncoded data sample:")
    print(df.head())
    
    # Prepare features and target
    X = df[['Age', 'BP', 'Cholesterol', 'Disease']]
    y = df['Drug']
    
    # Train decision tree
    print("\nTraining Decision Tree Classifier...")
    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=6,
        min_samples_split=5,
        min_samples_leaf=2
    )
    model.fit(X, y)
    
    # Save model with all encoders as a package
    model_data = {
        'model': model,
        'le_bp': le_bp,
        'le_chol': le_chol,
        'le_disease': le_disease,
        'le_drug': le_drug,
        'features': ['Age', 'BP', 'Cholesterol', 'Disease']
    }
    
    joblib.dump(model_data, model_path)
    print(f"\n✓ Model and encoders saved to: {model_path}")
    
    # Model information
    print(f"\n{'=' * 60}")
    print("MODEL TRAINING COMPLETE")
    print(f"{'=' * 60}")
    print(f"Model Type: Decision Tree Classifier")
    print(f"Model Depth: {model.get_depth()}")
    print(f"Number of leaves: {model.get_n_leaves()}")
    print(f"Training accuracy: {model.score(X, y):.4f}")
    print(f"Number of features: {len(X.columns)}")
    print(f"Features: {', '.join(X.columns)}")
    print(f"Output classes: {le_drug.classes_.tolist()}")
    
    # Test predictions
    print(f"\n{'=' * 60}")
    print("TEST PREDICTIONS")
    print(f"{'=' * 60}")
    
    test_cases = [
        {'age': 45, 'bp': 'HIGH', 'cholesterol': 'HIGH', 'disease': 'Hypertension'},
        {'age': 30, 'bp': 'LOW', 'cholesterol': 'NORMAL', 'disease': 'Fever'},
        {'age': 50, 'bp': 'NORMAL', 'cholesterol': 'HIGH', 'disease': 'Diabetes'},
        {'age': 25, 'bp': 'LOW', 'cholesterol': 'NORMAL', 'disease': 'Allergy'},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            age = test_case['age']
            bp_encoded = le_bp.transform([test_case['bp']])[0]
            chol_encoded = le_chol.transform([test_case['cholesterol']])[0]
            disease_encoded = le_disease.transform([test_case['disease']])[0]
            
            features = np.array([[age, bp_encoded, chol_encoded, disease_encoded]])
            prediction = model.predict(features)[0]
            predicted_drug = le_drug.inverse_transform([prediction])[0]
            
            print(f"Test {i}: Age={age}, BP={test_case['bp']}, Chol={test_case['cholesterol']}, Disease={test_case['disease']}")
            print(f"         → Predicted Drug: {predicted_drug}")
        except Exception as e:
            print(f"Test {i}: Error - {e}")
    
    print(f"\n{'=' * 60}")
    print("✓ MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    try:
        train_model()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error during model training: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

