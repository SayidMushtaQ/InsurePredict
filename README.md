# 🏥 Insurance Premium Category Prediction

A Machine Learning project that predicts an individual's **insurance premium category** based on personal, financial, lifestyle, and demographic features.

The project uses **Scikit-learn** to preprocess the data and train a **Random Forest classification model**.

---

## 🎯 Project Objective

The goal of this project is to predict the insurance premium category of a person based on their personal, financial, lifestyle, and demographic information.

The model predicts categories such as:

* 🟢 Low
* 🟡 Medium
* 🔴 High

This project demonstrates a complete beginner-friendly Machine Learning workflow:

**Data → Feature Engineering → Preprocessing → Model Training → Evaluation → Prediction**

---

## 🚀 Live Demo

The project consists of a **FastAPI backend** and a **Streamlit web application**.

### 🔹 FastAPI Backend

The backend is deployed on **Render** and provides the API required for making insurance premium predictions.

👉 **Backend API:**
https://insurepredict-jyjj.onrender.com

### 🔹 Streamlit Web Application

The user-facing application is built with **Streamlit** and connects to the deployed FastAPI backend.

👉 **Live Website:**
https://insurepredictgit-fh3zws7yhtpz4qtaxxrmbl.streamlit.app/

### ▶️ How to Run

To use the deployed application:

1. Make sure the **FastAPI backend** is running and accessible:
   `https://insurepredict-jyjj.onrender.com`
2. Open the **Streamlit application**:
   `https://insurepredictgit-fh3zws7yhtpz4qtaxxrmbl.streamlit.app/`
3. Enter the required user information.
4. The Streamlit application sends the input to the FastAPI backend.
5. The backend processes the data using the trained Machine Learning model.
6. The predicted insurance premium category is returned and displayed on the website.

> **Note:** The Streamlit application relies on the deployed FastAPI backend for prediction requests. Make sure the backend is available before using the web application.

---

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Matplotlib**
* **Seaborn**
* **Joblib**
* **FastAPI**
* **Streamlit**
* **Jupyter Notebook**
* **Render**

---

## 📂 Project Structure

```text
insurance-premium-prediction/
│
├── myenv/
│
├── dataset/
│   └── insurance.csv
│
├── model/
│   └── model.pkl
│
├── notebook/
│   └── insurance_prediction.ipynb
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🤖 Machine Learning Model

The project uses a **Random Forest Classifier** to predict the insurance premium category.

The workflow includes:

1. Data collection and exploration
2. Data preprocessing
3. Feature engineering
4. Encoding categorical features
5. Model training
6. Model evaluation
7. Model serialization using **Joblib**
8. Prediction through a **FastAPI API**
9. Integration with a **Streamlit frontend**

---

## 🔗 Project Links

* **GitHub Repository:** https://github.com/SayidMushtaQ/InsurePredict
* **Live Streamlit App:** https://insurepredictgit-fh3zws7yhtpz4qtaxxrmbl.streamlit.app/
* **FastAPI Backend:** https://insurepredict-jyjj.onrender.com

---

## 📌 Disclaimer

This project is created for **educational and demonstration purposes**. The predictions should not be considered professional financial or insurance advice.
