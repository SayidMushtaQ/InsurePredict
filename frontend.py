import streamlit as st
import requests

API_URL = "https://insurepredict-jyjj.onrender.com/predict"
BACKEND_URL = "https://insurepredict-jyjj.onrender.com"
FRONTEND_URL = "https://insurepredictgit-fh3zws7yhtpz4qtaxxrmbl.streamlit.app/"


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

st.markdown(
    "Enter your personal, financial, lifestyle, and demographic "
    "details below to predict the insurance premium category."
)


# -----------------------------
# How to Run / Instructions
# -----------------------------
with st.expander("⚙️ How to Use This Application", expanded=True):

    st.markdown("""
    ### 🚀 Application Instructions

    This application uses a **Streamlit frontend** connected to a
    **FastAPI backend** for making predictions.

    **Step 1 — Backend**

    The FastAPI backend is deployed on Render and must be accessible
    before making a prediction.

    **Backend:**  
    https://insurepredict-jyjj.onrender.com

    **Step 2 — Frontend**

    This Streamlit application provides the user interface for entering
    information and receiving predictions.

    **Live App:**  
    https://insurepredictgit-fh3zws7yhtpz4qtaxxrmbl.streamlit.app/

    **Step 3 — Enter Your Details**

    Provide the following information:

    - Age
    - Weight
    - Height
    - Annual Income
    - Smoking status
    - City
    - Occupation

    **Step 4 — Get Your Prediction**

    Click **🔮 Predict Premium Category**.

    The Streamlit application sends your information to the FastAPI
    backend, which processes it using the trained Machine Learning model
    and returns the predicted premium category.

    > ⚠️ **Important:** The frontend depends on the FastAPI backend.
    > If the backend is unavailable, predictions cannot be generated.

    ### 🔄 If the Application Does Not Respond

    The backend is hosted on Render and may take a short time to wake up
    if it has been inactive.

    If you receive a connection or timeout error:

    1. Open the backend URL:
       https://insurepredict-jyjj.onrender.com
    2. Wait a few seconds for the server to respond.
    3. Return to this application.
    4. Try the prediction again.
    """)


# -----------------------------
# Backend Information
# -----------------------------
st.info(
    "🔗 This application is connected to the deployed FastAPI backend."
)

st.caption(
    f"FastAPI Backend: {BACKEND_URL}"
)


# -----------------------------
# Input Fields
# -----------------------------
st.subheader("📝 Enter Your Information")

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
    options=[True, False],
    format_func=lambda x: "Yes" if x else "No"
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
if st.button(
    "🔮 Predict Premium Category",
    use_container_width=True
):

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

    # Show loading message while contacting API
    with st.spinner("🔄 Connecting to the prediction server..."):

        try:

            # Send request to FastAPI
            response = requests.post(
                API_URL,
                json=input_data,
                timeout=30
            )

            # Try to convert response to JSON
            try:
                result = response.json()
            except ValueError:
                result = None

            # -----------------------------
            # Successful Response
            # -----------------------------
            if response.status_code == 200:

                prediction = result["predicted_category"]

                st.success(
                    f"🎯 Predicted Insurance Premium Category: "
                    f"**{prediction}**"
                )

                if "Message" in result:
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

                if result:
                    st.json(result)
                else:
                    st.code(response.text)

        # -----------------------------
        # Connection Error
        # -----------------------------
        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the FastAPI server."
            )

            st.warning(
                "Please make sure the FastAPI backend is available at:"
            )

            st.code(BACKEND_URL)

            st.markdown(
                "👉 **Try opening the backend URL first, wait a few "
                "seconds, and then try the prediction again.**"
            )

        # -----------------------------
        # Timeout Error
        # -----------------------------
        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The request timed out."
            )

            st.warning(
                "The Render backend may be waking up. "
                "Please wait a few seconds and try again."
            )

        # -----------------------------
        # Other Request Errors
        # -----------------------------
        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Request error: {e}"
            )

        # -----------------------------
        # Invalid JSON Response
        # -----------------------------
        except ValueError:

            st.error(
                "❌ FastAPI returned an invalid JSON response."
            )


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "🏥 Insurance Premium Category Prediction | "
    "Machine Learning + FastAPI + Streamlit"
)
