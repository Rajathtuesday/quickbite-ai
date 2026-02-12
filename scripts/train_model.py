# import json
# import os
# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.metrics import classification_report
# import joblib

# DATA_FILE = "logs/training_data.jsonl"
# MODEL_FILE = "models/recommender_v1.pkl"

# rows = []

# # -----------------------------
# # Load data
# # -----------------------------
# with open(DATA_FILE, "r", encoding="utf-8") as f:
#     for line in f:
#         rows.append(json.loads(line))

# df = pd.DataFrame(rows)

# # -----------------------------
# # Target label
# # -----------------------------
# df["label"] = df["clicked"]

# # -----------------------------
# # Interaction feature
# # -----------------------------
# df["context_combo"] = df["situation"] + "_" + df["craving"]

# # -----------------------------
# # Features (NO RANK ANYMORE)
# # -----------------------------
# features = [
#     "city",
#     "context_combo",
#     "dish_id"
# ]

# X = df[features]
# y = df["label"]

# # -----------------------------
# # Preprocessing
# # -----------------------------
# categorical = ["city", "context_combo", "dish_id"]

# preprocessor = ColumnTransformer(
#     transformers=[
#         ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
#     ]
# )

# # -----------------------------
# # Model
# # -----------------------------
# model = LogisticRegression(
#     max_iter=1000,
#     class_weight="balanced"
# )

# pipeline = Pipeline(
#     steps=[
#         ("preprocessor", preprocessor),
#         ("model", model),
#     ]
# )

# # -----------------------------
# # Train
# # -----------------------------
# pipeline.fit(X, y)

# # -----------------------------
# # Evaluate
# # -----------------------------
# preds = pipeline.predict(X)
# print(classification_report(y, preds))

# # -----------------------------
# # Save model
# # -----------------------------
# os.makedirs("models", exist_ok=True)
# joblib.dump(pipeline, MODEL_FILE)
# print(f"✅ Model saved to {MODEL_FILE}")
# ================================================================
import json
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

DATA_FILE = "logs/training_data.jsonl"
MODEL_FILE = "models/recommender_v2.pkl"

rows = []

with open(DATA_FILE, "r", encoding="utf-8") as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows)

y = df["clicked"]

categorical = ["city", "context_combo"]
numeric = [
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
    "price_bucket"
]

X = df[categorical + numeric]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric),
    ]
)

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)

pipeline.fit(X, y)

preds = pipeline.predict(X)
print(classification_report(y, preds))

os.makedirs("models", exist_ok=True)
joblib.dump(pipeline, MODEL_FILE)

print("✅ Model saved to models/recommender_v2.pkl")
