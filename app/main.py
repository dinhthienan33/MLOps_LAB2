from flask import Flask, request, jsonify
import os
import logging
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Model path from environment variable
MODEL_PATH = os.getenv("MODEL_PATH", "../models/Logistic_Model.pkl")

# Feature columns
COLUMNS = ['battery_power', 'blue', 'clock_speed', 'dual_sim', 
          'fc', 'four_g', 'int_memory', 'm_dep', 'mobile_wt', 
          'n_cores', 'pc', 'px_height', 'px_width', 'ram',
          'sc_h', 'sc_w', 'talk_time', 'three_g', 'touch_screen', 'wifi']

# Price categories
PRICE_CATEGORIES = {
    0: "Low Cost",
    1: "Medium Cost",
    2: "High Cost",
    3: "Very High Cost"
}

# Load model
try:
    logger.info(f"Loading model from {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

def predict_price_category(features_dict):
    """
    Predict mobile price category based on features
    """
    # Convert input dictionary to dataframe
    df = pd.DataFrame([features_dict])
    
    # Ensure all required columns are present
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = 0
    
    # Select only needed columns and ensure correct order
    df = df[COLUMNS]
    
    # Scale the features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(df)
    
    # Make prediction
    predicted_class = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    
    return int(predicted_class), probabilities.tolist(), PRICE_CATEGORIES.get(int(predicted_class), "Unknown")

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify if the service is running
    """
    return jsonify({"status": "ok", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the price category of a mobile phone based on its features
    """
    # Ensure model is loaded
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get JSON data from request
        features_dict = request.get_json()
        
        # Validate required fields
        for field in COLUMNS:
            if field not in features_dict:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Make prediction
        predicted_class, probabilities, category_name = predict_price_category(features_dict)
        
        # Create response with class probabilities
        response = {
            "price_category": predicted_class,
            "category_name": category_name,
            "probabilities": {str(i): float(prob) for i, prob in enumerate(probabilities)}
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """
    Predict the price category for multiple mobile phones
    """
    # Ensure model is loaded
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get JSON data from request
        features_list = request.get_json()
        
        if not isinstance(features_list, list):
            return jsonify({"error": "Request body must be a JSON array"}), 400
        
        results = []
        for features_dict in features_list:
            # Validate required fields
            for field in COLUMNS:
                if field not in features_dict:
                    return jsonify({"error": f"Missing required field: {field} in one of the items"}), 400
            
            predicted_class, probabilities, category_name = predict_price_category(features_dict)
            
            results.append({
                "price_category": predicted_class,
                "category_name": category_name,
                "probabilities": {str(i): float(prob) for i, prob in enumerate(probabilities)}
            })
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({"error": f"Batch prediction error: {str(e)}"}), 500


if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    app.run(host=host, port=port)