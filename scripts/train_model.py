import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os

DATA_PATH = "logs/training_data.jsonl"
MODEL_PATH = "models/recommender_v2.pkl"

print("Loading training data...")

df = pd.read_json(DATA_PATH, lines=True)

print("Columns in dataset:", df.columns)

# -----------------------------
# Determine target column
# -----------------------------
if "ordered" in df.columns:
    target_col = "ordered"
elif "clicked" in df.columns:
    target_col = "clicked"
else:
    raise RuntimeError("No target column found (clicked/ordered missing).")

print(f"Using target column: {target_col}")

df["label"] = df[target_col]

# -----------------------------
# Feature Columns
# -----------------------------
categorical_features = ["city", "context_combo"]

numeric_features = [
    "is_spicy",
    "is_creamy",
    "is_sweet",
    "is_fried",
    "is_healthy",
    "is_indulgent",
    "is_south_indian",
    "is_north_indian",
    "is_street_food",
    "popularity",
    "price_bucket",
]

X = df[categorical_features + numeric_features]
y = df["label"]

# -----------------------------
# Train/Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Preprocessing
# -----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
)
    ]
)

print("Training model...")
model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = model.predict(X_test)
print("\n=== MODEL PERFORMANCE ===")
print(classification_report(y_test, y_pred))

# -----------------------------
# Save Model
# -----------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\n✅ Model saved to {MODEL_PATH}")
