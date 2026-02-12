import joblib
import os

MODEL_PATH = "models/recommender_v2.pkl"
_model = None

def get_model():
    global _model

    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        raise RuntimeError("Model file not found. Train model first.")

    try:
        _model = joblib.load(MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

    return _model
