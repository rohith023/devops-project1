"""
Machine Learning Model Training Script
Trains a Decision Tree Classifier for drug recommendation
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
data_path = os.path.join(project_root, 'data', 'drug200.csv')
model_path = os.path.join(project_root, 'model.pkl')

def train_model():
    """Train the decision tree model and save it"""
    print("Loading data from:", data_path)
    
    # Load data
    df = pd.read_csv(data_path)
    print(f"Data shape: {df.shape}")
    print(f"Data columns: {df.columns.tolist()}")
    
    # Encode categorical features
    le_bp = LabelEncoder()
    le_chol = LabelEncoder()
    le_drug = LabelEncoder()
    
    df['BP'] = le_bp.fit_transform(df['BP'])
    df['Cholesterol'] = le_chol.fit_transform(df['Cholesterol'])
    df['Drug'] = le_drug.fit_transform(df['Drug'])
    
    print("\nEncoded data sample:")
    print(df.head())
    
    # Prepare features and target
    X = df[['Age', 'BP', 'Cholesterol']]
    y = df['Drug']
    
    # Train decision tree
    print("\nTraining Decision Tree Classifier...")
    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=2
    )
    model.fit(X, y)
    
    # Save model with encoders
    model_data = {
        'model': model,
        'le_bp': le_bp,
        'le_chol': le_chol,
        'le_drug': le_drug
    }
    
    joblib.dump(model_data, model_path)
    print(f"\nModel saved to: {model_path}")
    
    # Model information
    print(f"\nModel Training Complete")
    print(f"Model Depth: {model.get_depth()}")
    print(f"Number of leaves: {model.get_n_leaves()}")
    print(f"Training accuracy: {model.score(X, y):.4f}")
    
    # Test predictions
    test_sample = np.array([[45, 1, 0]])  # Age=45, BP=LOW, Cholesterol=NORMAL
    prediction = model.predict(test_sample)
    predicted_drug = le_drug.inverse_transform(prediction)[0]
    print(f"\nSample prediction: Age=45, BP=LOW, Cholesterol=NORMAL -> {predicted_drug}")

if __name__ == "__main__":
    try:
        train_model()
        print("\n✓ Model training completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error during model training: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
