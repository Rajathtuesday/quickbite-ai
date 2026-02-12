import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/v1/recommend"

st.set_page_config(page_title="QuickBite AI", layout="centered")

st.title("🍽 QuickBite AI")
st.subheader("Smart food recommendations in 3 questions")

city = st.selectbox("City", ["bangalore"])

situation = st.selectbox(
    "What’s your situation?",
    ["office_lunch", "treat_myself", "lazy_tired", "light_healthy", "evening_snack", "celebration"]
)

craving = st.selectbox(
    "What are you craving?",
    ["spicy", "creamy", "sweet", "healthy", "fried"]
)

constraints = st.multiselect(
    "Any constraints?",
    ["veg_only", "under_250"]
)

if st.button("Get Recommendation"):
    payload = {
        "city": city,
        "session_id": "demo_ui_session",
        "answers": {
            "situation": situation,
            "craving": craving,
            "constraints": constraints
        }
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        st.success("Top Picks For You")

        for dish in data["top_picks"]:
            st.markdown(f"### 🍴 {dish['name']}")
            st.write(f"Confidence Score: {dish['score']}")
            st.write("---")
    else:
        st.error("API error. Is FastAPI running?")
