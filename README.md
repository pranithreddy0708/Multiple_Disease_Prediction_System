# 🏥 Multiple Disease Prediction System

An AI-powered web application built with **Flask**, **Scikit-Learn**, and **SQLite** to predict multiple health conditions based on user-inputted clinical features.

---

## 🌐 Live Server

The application is currently running locally on:
* **Local Web Server**: [http://127.0.0.1:5100/](http://127.0.0.1:5100/) or [http://localhost:5100/](http://localhost:5100/)

---

## ✨ Features

- **Diabetes Prediction**: Analyzes glucose, blood pressure, insulin, BMI, etc.
- **Heart Disease Prediction**: Evaluates chest pain type, resting BP, cholesterol, maximum heart rate, and ST depression.
- **Parkinson's Disease Prediction**: Uses vocal measurement metrics to detect early signs of Parkinson's.
- **Lung Cancer Prediction**: Evaluates lifestyle factors, age, and respiratory symptoms.
- **Kidney Disease Prediction**: Assesses serum creatinine, blood urea, hemoglobin, sodium, and potassium levels.
- **Symptom Checker**: Interactive tool for checking general symptoms.
- **User Authentication**: Secure user registration and login system backed by SQLite database.
- **Prediction History**: Track past prediction results over time.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Flask 3.1, Flask-SQLAlchemy, Joblib
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/pranithreddy0708/Multiple_Disease_Prediction_System.git
cd Multiple_Disease_Prediction_System
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5100/`.

---

## 📁 Repository Structure

```
├── app.py                  # Main Flask server & route handlers
├── train_models.py         # Machine learning model training script
├── fix_heart.py            # Utility script for model adjustments
├── requirements.txt        # Python package dependencies
├── datasets/               # Training datasets (CSV)
├── models/                 # Pre-trained ML models & scalers (.pkl)
├── static/                 # CSS styles and JavaScript assets
├── templates/              # HTML templates (Jinja2)
└── README.md               # Project documentation
```
