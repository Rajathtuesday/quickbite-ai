import joblib

MODEL_PATH = "models/recommender_v2.pkl"

_model = None

def get_model():
    global _model

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    return _model
