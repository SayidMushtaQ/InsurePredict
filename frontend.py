import streamlit as st
import requests


# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = "http://54.234.31.162:8000/predict"
BACKEND_URL = "http://54.234.31.162:8000/"
FRONTEND_URL = "https://insurepredictgit-fh3zws7yhtpz4qtaxxrmbl.streamlit.app/"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="💰",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("💰 Insurance Premium Category Predictor")

st.markdown(
    """
    Enter your personal, financial, lifestyle, and demographic
    information to predict your insurance premium category.
    """
)


# ============================================================
# HOW TO USE
# ============================================================

with st.expander("⚙️ How to Use This Application", expanded=False):

    st.markdown(
        """
        ### 🚀 Application Instructions

        This application uses a **Streamlit frontend** connected to
        a **FastAPI backend** and a trained Machine Learning model.

        ### Step 1 — Backend

        The prediction API is hosted on AWS.

        **Backend:**

        `http://54.234.31.162:8000/`

        ### Step 2 — Enter Your Details

        Provide:

        - Age
        - Weight
        - Height
        - Annual Income
        - Lifestyle Risk
        - City Tier
        - Occupation

        BMI and age group are calculated automatically.

        ### Step 3 — Get Your Prediction

        Click:

        **🔮 Predict Premium Category**

        The Streamlit application sends your information to the
        FastAPI backend.

        The backend processes the data using the trained ML model
        and returns:

        - Predicted premium category
        - Confidence score
        - Probability for each category

        ### ⚠️ Important

        The frontend depends on the FastAPI backend being available.

        If the backend is unavailable, predictions cannot be generated.
        """
    )


# ============================================================
# BACKEND INFORMATION
# ============================================================

st.info(
    "🔗 This application is connected to the deployed FastAPI backend."
)

st.caption(
    f"FastAPI Backend: {BACKEND_URL}"
)


# ============================================================
# USER INFORMATION
# ============================================================

st.subheader("📝 Enter Your Information")


# ------------------------------------------------------------
# Age
# ------------------------------------------------------------

age = st.number_input(
    "Age",
    min_value=1,
    max_value=119,
    value=30,
    step=1
)


# ------------------------------------------------------------
# Automatically calculate age group
# ------------------------------------------------------------

def get_age_group(age):
    if age < 18:
        return "young"
    elif age < 30:
        return "young_adult"
    elif age < 45:
        return "adult"
    elif age < 60:
        return "middle_aged"
    else:
        return "senior"


age_group = get_age_group(age)

st.caption(f"👤 Age Group: **{age_group}**")


# ============================================================
# HEIGHT & WEIGHT
# ============================================================

col1, col2 = st.columns(2)


with col1:

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=300.0,
        value=65.0,
        step=0.1
    )


with col2:

    height = st.number_input(
        "Height (m)",
        min_value=0.5,
        max_value=2.5,
        value=1.70,
        step=0.01
    )


# ------------------------------------------------------------
# BMI Calculation
# ------------------------------------------------------------

bmi = weight / (height ** 2)

st.metric(
    label="⚖️ Calculated BMI",
    value=f"{bmi:.2f}"
)


# ============================================================
# INCOME
# ============================================================

income_lpa = st.number_input(
    "💵 Annual Income (LPA)",
    min_value=0.1,
    max_value=1000.0,
    value=10.0,
    step=0.1
)


# ============================================================
# LIFESTYLE RISK
# ============================================================

lifestyle_risk = st.selectbox(
    "🏃 Lifestyle Risk",
    options=[
        "low",
        "medium",
        "high"
    ]
)


# ============================================================
# CITY TIER
# ============================================================

city_tier = st.selectbox(
    "🏙️ City Tier",
    options=[
        "tier_1",
        "tier_2",
        "tier_3"
    ]
)


# ============================================================
# OCCUPATION
# ============================================================

occupation = st.selectbox(
    "💼 Occupation",
    options=[
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)


# ============================================================
# SHOW INPUT SUMMARY
# ============================================================

with st.expander("📋 View Calculated Input Data"):

    input_preview = {
        "bmi": round(bmi, 2),
        "age_group": age_group,
        "lifestyle_risk": lifestyle_risk,
        "city_tier": city_tier,
        "income_lpa": income_lpa,
        "occupation": occupation
    }

    st.json(input_preview)


# ============================================================
# PREDICTION BUTTON
# ============================================================

if st.button(
    "🔮 Predict Premium Category",
    use_container_width=True
):

    # --------------------------------------------------------
    # Data sent to FastAPI
    # --------------------------------------------------------

    input_data = {
        "bmi": round(bmi, 2),
        "age_group": age_group,
        "lifestyle_risk": lifestyle_risk,
        "city_tier": city_tier,
        "income_lpa": income_lpa,
        "occupation": occupation
    }


    # --------------------------------------------------------
    # API Request
    # --------------------------------------------------------

    with st.spinner(
        "🔄 Connecting to the prediction server..."
    ):

        try:

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=30
            )


            # ------------------------------------------------
            # Convert response to JSON
            # ------------------------------------------------

            try:

                result = response.json()

            except ValueError:

                result = None


            # =================================================
            # SUCCESS
            # =================================================

            if response.status_code == 200:

                if result is None:

                    st.error(
                        "❌ The API returned an invalid response."
                    )

                else:

                    # ----------------------------------------
                    # Extract prediction
                    # ----------------------------------------

                    prediction = result.get(
                        "predicted_category"
                    )

                    confidence = result.get(
                        "confidence"
                    )

                    class_probabilities = result.get(
                        "class_probabilities",
                        {}
                    )


                    # ----------------------------------------
                    # Prediction Result
                    # ----------------------------------------

                    st.success(
                        f"🎯 Predicted Insurance Premium Category: "
                        f"**{prediction}**"
                    )


                    # ----------------------------------------
                    # Confidence
                    # ----------------------------------------

                    if confidence is not None:

                        st.metric(
                            "🎯 Model Confidence",
                            f"{confidence * 100:.2f}%"
                        )


                    # ----------------------------------------
                    # Probability Distribution
                    # ----------------------------------------

                    if class_probabilities:

                        st.subheader(
                            "📊 Class Probabilities"
                        )

                        # Convert probabilities to percentages

                        probability_data = {
                            category: probability * 100
                            for category, probability
                            in class_probabilities.items()
                        }

                        st.bar_chart(
                            probability_data
                        )


                        # Show exact values

                        for category, probability in (
                            class_probabilities.items()
                        ):

                            st.write(
                                f"**{category}:** "
                                f"{probability * 100:.2f}%"
                            )


                    # ----------------------------------------
                    # Input Data
                    # ----------------------------------------

                    with st.expander(
                        "📋 View Submitted Input"
                    ):

                        st.json(input_data)


                    # ----------------------------------------
                    # API Response
                    # ----------------------------------------

                    with st.expander(
                        "🔍 View API Response"
                    ):

                        st.json(result)


            # =================================================
            # API ERROR
            # =================================================

            else:

                st.error(
                    f"❌ API Error: {response.status_code}"
                )

                if result:

                    st.json(result)

                else:

                    st.code(response.text)


        # =====================================================
        # CONNECTION ERROR
        # =====================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the FastAPI server."
            )

            st.warning(
                "Please make sure the FastAPI backend is "
                "running and accessible."
            )

            st.code(
                BACKEND_URL
            )

            st.markdown(
                """
                👉 Try opening the backend URL first.
                If the server is starting up, wait a few seconds
                and try the prediction again.
                """
            )


        # =====================================================
        # TIMEOUT ERROR
        # =====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The request timed out."
            )

            st.warning(
                "The FastAPI server took too long to respond. "
                "Please try again."
            )


        # =====================================================
        # OTHER REQUEST ERROR
        # =====================================================

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Request error: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏥 Insurance Premium Category Prediction | "
    "Machine Learning + FastAPI + Streamlit"
)