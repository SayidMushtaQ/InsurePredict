import streamlit as st
import requests

API_URL = "https://insurepredict-jyjj.onrender.com/predict"


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="💰",
    layout="centered"
)


# -----------------------------
# Title
# -----------------------------
st.title("💰 Insurance Premium Category Predictor")
st.markdown("Enter your details below to predict the insurance premium category.")


# -----------------------------
# Input Fields
# -----------------------------
age = st.number_input(
    "Age",
    min_value=1,
    max_value=119,
    value=30,
    step=1
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    value=65.0,
    step=0.1
)

height = st.number_input(
    "Height (m)",
    min_value=0.5,
    max_value=2.5,
    value=1.7,
    step=0.01
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.1,
    value=10.0,
    step=0.1
)

smoker = st.selectbox(
    "Are you a smoker?",
    options=[True, False]
)

city = st.text_input(
    "City",
    value="Mumbai"
)

occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)


# -----------------------------
# Prediction Button
# -----------------------------
if st.button("🔮 Predict Premium Category", use_container_width=True):

    # Data sent to FastAPI
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:

        # Send request to FastAPI
        response = requests.post(
            API_URL,
            json=input_data,
            timeout=10
        )

        # Convert response to JSON
        result = response.json()

        # -----------------------------
        # Successful Response
        # -----------------------------
        if response.status_code == 200:

            prediction = result["predicted_category"]

            st.success(
                f"🎯 Predicted Insurance Premium Category: "
                f"**{prediction}**"
            )

            st.info(result["Message"])

            # Show submitted information
            with st.expander("📋 View Input Data"):
                st.json(input_data)

            # Show API response
            with st.expander("🔍 View API Response"):
                st.json(result)

        # -----------------------------
        # API Error
        # -----------------------------
        else:

            st.error(
                f"❌ API Error: {response.status_code}"
            )

            st.json(result)

    # -----------------------------
    # Connection Error
    # -----------------------------
    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI server.\n\n"
            "Make sure your FastAPI server is running on "
            "https://insurepredict-jyjj.onrender.com"
        )

    # -----------------------------
    # Timeout Error
    # -----------------------------
    except requests.exceptions.Timeout:

        st.error(
            "⏱️ Request timed out. "
            "Please check whether the FastAPI server is running."
        )

    # -----------------------------
    # Other Request Errors
    # -----------------------------
    except requests.exceptions.RequestException as e:

        st.error(f"❌ Request error: {e}")

    # -----------------------------
    # Invalid JSON Response
    # -----------------------------
    except ValueError:

        st.error(
            "❌ FastAPI returned an invalid JSON response."
        )