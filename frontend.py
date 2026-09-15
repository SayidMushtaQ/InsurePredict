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
    details below to predict your insurance premium category.
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

        The FastAPI prediction API is deployed on AWS.

        **Backend:**

        `http://54.234.31.162:8000/`

        ### Step 2 — Enter Your Details

        Provide the following information:

        - Age
        - Weight
        - Height
        - Annual Income
        - Lifestyle Risk
        - City Tier
        - Occupation

        **BMI** and **Age Group** are calculated automatically.

        ### Step 3 — Get Your Prediction

        Click:

        **🔮 Predict Premium Category**

        The Streamlit application sends the information to the
        FastAPI backend.

        The Machine Learning model returns:

        - Predicted premium category
        - Model confidence
        - Probability for each class

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
# AGE GROUP FUNCTION
# ============================================================

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


# ============================================================
# USER INFORMATION
# ============================================================

st.subheader("📝 Enter Your Information")


# ============================================================
# AGE
# ============================================================

age = st.number_input(
    "Age",
    min_value=1,
    max_value=119,
    value=30,
    step=1
)


# ============================================================
# AGE GROUP
# ============================================================

age_group = get_age_group(age)

st.caption(
    f"👤 Age Group: **{age_group}**"
)


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


# ============================================================
# BMI CALCULATION
# ============================================================

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
# INPUT PREVIEW
# ============================================================

with st.expander("📋 View Input Data", expanded=False):

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

    # ========================================================
    # DATA SENT TO FASTAPI
    # ========================================================

    input_data = {
        "bmi": round(bmi, 2),
        "age_group": age_group,
        "lifestyle_risk": lifestyle_risk,
        "city_tier": city_tier,
        "income_lpa": income_lpa,
        "occupation": occupation
    }


    # ========================================================
    # API REQUEST
    # ========================================================

    with st.spinner(
        "🔄 Connecting to the prediction server..."
    ):

        try:

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=30
            )


            # ====================================================
            # PARSE JSON
            # ====================================================

            try:

                result = response.json()

            except ValueError:

                result = None


            # ====================================================
            # SUCCESS
            # ====================================================

            if response.status_code == 200:

                if result is None:

                    st.error(
                        "❌ The FastAPI server returned an invalid "
                        "JSON response."
                    )

                    st.code(response.text)

                else:

                    # ============================================
                    # HANDLE NEW API RESPONSE
                    # ============================================

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


                    # ============================================
                    # HANDLE OLD/NESTED RESPONSE
                    #
                    # This protects the frontend if the AWS
                    # backend is still running an older version.
                    # ============================================

                    if (
                        prediction is None
                        and isinstance(result.get("response"), dict)
                    ):

                        prediction_result = result["response"]

                        prediction = prediction_result.get(
                            "predicted_category"
                        )

                        confidence = prediction_result.get(
                            "confidence"
                        )

                        class_probabilities = (
                            prediction_result.get(
                                "class_probabilities",
                                {}
                            )
                        )


                    # ============================================
                    # CHECK RESPONSE
                    # ============================================

                    if prediction is None:

                        st.error(
                            "❌ Prediction was not found in the API "
                            "response."
                        )

                        st.warning(
                            "The API responded successfully, but the "
                            "response format is different from expected."
                        )

                        with st.expander(
                            "🔍 View Raw API Response",
                            expanded=True
                        ):

                            st.json(result)


                    else:

                        # ========================================
                        # PREDICTION RESULT
                        # ========================================

                        st.success(
                            f"🎯 Predicted Insurance Premium Category: "
                            f"**{prediction}**"
                        )


                        # ========================================
                        # CONFIDENCE
                        # ========================================

                        if confidence is not None:

                            st.subheader(
                                "🎯 Prediction Confidence"
                            )

                            st.progress(
                                float(confidence)
                            )

                            st.write(
                                f"Model confidence: "
                                f"**{confidence * 100:.2f}%**"
                            )


                        # ========================================
                        # CLASS PROBABILITIES
                        # ========================================

                        if class_probabilities:

                            st.subheader(
                                "📊 Class Probabilities"
                            )


                            # ------------------------------------
                            # Convert to percentage
                            # ------------------------------------

                            probability_data = {
                                category: probability * 100
                                for category, probability
                                in class_probabilities.items()
                            }


                            # ------------------------------------
                            # Chart
                            # ------------------------------------

                            st.bar_chart(
                                probability_data
                            )


                            # ------------------------------------
                            # Exact values
                            # ------------------------------------

                            for (
                                category,
                                probability
                            ) in class_probabilities.items():

                                st.write(
                                    f"**{category}:** "
                                    f"{probability * 100:.2f}%"
                                )


                        # ========================================
                        # SUBMITTED DATA
                        # ========================================

                        with st.expander(
                            "📋 View Submitted Input",
                            expanded=False
                        ):

                            st.json(input_data)


                        # ========================================
                        # RAW API RESPONSE
                        # ========================================

                        with st.expander(
                            "🔍 View API Response",
                            expanded=False
                        ):

                            st.json(result)


            # ====================================================
            # API ERROR
            # ====================================================

            else:

                st.error(
                    f"❌ API Error: {response.status_code}"
                )


                if result:

                    st.json(result)

                else:

                    st.code(response.text)


        # ========================================================
        # CONNECTION ERROR
        # ========================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the FastAPI server."
            )

            st.warning(
                "Please make sure your AWS FastAPI server is "
                "running and accessible."
            )

            st.code(
                BACKEND_URL
            )


        # ========================================================
        # TIMEOUT ERROR
        # ========================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The request timed out."
            )

            st.warning(
                "The FastAPI server took too long to respond. "
                "Please try again."
            )


        # ========================================================
        # OTHER REQUEST ERROR
        # ========================================================

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