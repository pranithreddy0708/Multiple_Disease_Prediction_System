from unittest import result

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import numpy as np
import joblib
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret123"

db = SQLAlchemy(app)


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(100), nullable=False)
    
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    password = db.Column(db.String(100), nullable=False)





# -------------------------
# Load models safely
# -------------------------
def load_model(name):
    mp = f"models/{name}_model.pkl"
    sp = f"models/{name}_scaler.pkl"
    if os.path.exists(mp) and os.path.exists(sp):
        return joblib.load(mp), joblib.load(sp)
    return None, None


diabetes_model, diabetes_scaler = load_model("diabetes")
heart_model, heart_scaler = load_model("heart_disease")
parkinsons_model, parkinsons_scaler = load_model("parkinsons")

lung_model = joblib.load("models/lung_cancer_model.pkl")
lung_scaler = joblib.load("models/lung_scaler.pkl")

kidney_model = joblib.load("models/kidney_disease_model.pkl")
kidney_scaler = joblib.load("models/kidney_scaler.pkl")


# -------------------------
# Pages
# -------------------------



@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/symptom-checker")
def symptom_checker():
    return render_template("symptom_checker.html")


@app.route("/diabetes")
def diabetes():
    return render_template("diabetes.html")


@app.route("/heart")
def heart():
    return render_template("heart.html")


@app.route("/parkinsons")
def parkinsons():
    return render_template("parkinsons.html")


@app.route("/lung")
def lung():
    return render_template("lung.html")


@app.route("/kidney")
def kidney():
    return render_template("kidney.html")


@app.route("/history")
def history():
    return render_template("history.html")


# -------------------------
# Diabetes
# -------------------------


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session["user"] = user.username
            return redirect(url_for("index"))
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    try:
        d = request.get_json()

        features = np.array([[ 
            d["pregnancies"], d["glucose"], d["blood_pressure"],
            d["skin_thickness"], d["insulin"], d["bmi"],
            d["dpf"], d["age"]
        ]])

        scaled = diabetes_scaler.transform(features)

        result = int(diabetes_model.predict(scaled)[0])
        prob = float(diabetes_model.predict_proba(scaled)[0][result])

        advice = "⚠️ Visit Doctor" if result == 1 else "✅ You are Safe"

        return jsonify({
            "prediction": result,
            "label": "Diabetic" if result == 1 else "Not Diabetic",
            "confidence": round(prob * 100, 1),
            "advice": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------
# Heart
# -------------------------
@app.route("/predict/heart", methods=["POST"])
def predict_heart():
    try:
        d = request.get_json()

        features = np.array([[ 
            d["age"], d["sex"], d["cp"], d["trestbps"],
            d["chol"], d["fbs"], d["restecg"],
            d["thalach"], d["exang"], d["oldpeak"],
            d["slope"], d["ca"], d["thal"]
        ]])

        scaled = heart_scaler.transform(features)

        result = int(heart_model.predict(scaled)[0])
        proba = heart_model.predict_proba(scaled)[0][1]   # probability of disease

# 🔥 Smart threshold + safety override
        if proba > 0.4 or d["oldpeak"] > 2 or d["chol"] > 280:
            result = 1
        else:
            result = 0

        prob = proba
        

        advice = "⚠️ Visit Doctor" if result == 1 else "✅ You are Safe"

        return jsonify({
            "prediction": result,
            "label": "Heart Disease Detected" if result == 1 else "No Heart Disease",
            "confidence": round(prob * 100, 1),
            "advice": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------
# Parkinsons
# -------------------------
@app.route("/predict/parkinsons", methods=["POST"])
def predict_parkinsons():
    try:
        d = request.get_json()

        keys = [
            "fo","fhi","flo","jitter_percent","jitter_abs","rap","ppq","ddp",
            "shimmer","shimmer_db","apq3","apq5","apq","dda","nhr","hnr",
            "rpde","dfa","spread1","spread2","d2","ppe"
        ]

        features = np.array([[d[k] for k in keys]])

        scaled = parkinsons_scaler.transform(features)

        result = int(parkinsons_model.predict(scaled)[0])
        proba = parkinsons_model.predict_proba(scaled)[0][1]  # disease probability

# Better threshold for Parkinson's (important)
        if proba > 0.6:
            result = 1
        elif proba > 0.4:
            result = 0   # treat borderline as safe
        else:
            result = 0

        prob = proba

        if prob > 0.6:
            advice = "⚠️ Visit Doctor"
        elif prob > 0.4:
            advice = "🟡 Moderate Risk - Monitor symptoms"
        else:
            advice = "✅ You are Safe"

        return jsonify({
            "prediction": result,
            "label": "Parkinson's Detected" if result == 1 else "No Parkinson's",
            "confidence": round(prob * 100, 1),
            "advice": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------
# Lung Cancer
# -------------------------
@app.route("/predict/lung", methods=["POST"])
def predict_lung():
    try:
        d = request.get_json()

        features = np.array([[ 
            d["age"],
            d["smoking"],
            d["yellow_fingers"],
            d["anxiety"],
            d["peer_pressure"],
            d["chronic_disease"],
            d["fatigue"],
            d["allergy"],
            d["wheezing"],
            d["alcohol_consuming"],
            d["coughing"],
            d["shortness_of_breath"],
            d["swallowing_difficulty"],
            d["chest_pain"]
        ]])

        scaled = lung_scaler.transform(features)

        proba = lung_model.predict_proba(scaled)[0][1]

# Smart threshold
        if proba > 0.4:
            prediction = 1
        else:
            prediction = 0

# 🚨 Rule-based override (VERY IMPORTANT)
        if d["smoking"] == 1 and d["coughing"] == 1 and d["shortness_of_breath"] == 1:
            prediction = 1

        confidence = proba * 100

        advice = "⚠️ Visit Doctor" if prediction == 1 else "✅ You are Safe"

        return jsonify({
            "prediction": int(prediction),
            "label": "Lung Cancer Detected" if prediction == 1 else "No Lung Cancer",
            "confidence": round(confidence, 1),
            "advice": advice
        })

    except Exception as e:
        print("LUNG ERROR:", e)
        return jsonify({"error": str(e)}), 400


# -------------------------
# Kidney
# -------------------------
@app.route("/predict/kidney", methods=["POST"])
def predict_kidney():
    try:
        d = request.get_json()

        features = np.array([[ 
            d["age"],
            d["bp"],
            d["sg"],
            d["al"],
            d["su"],
            d["bgr"],
            d["bu"],
            d["sc"],
            d["sod"],
            d["pot"],
            d["hemo"],
            d["pcv"]
        ]])

        scaled = kidney_scaler.transform(features)

        result = int(kidney_model.predict(scaled)[0])
        proba = kidney_model.predict_proba(scaled)[0][1]

# 🚨 Rule 1: Strong abnormal indicators → disease
        if d["sc"] > 2 or d["bu"] > 60 or d["hemo"] < 10:
            prediction = 1

# ✅ Rule 2: Mostly normal values → SAFE (override model)
        elif (
            d["sc"] <= 1.5 and
            d["bu"] < 40 and
            d["hemo"] >= 12 and
            d["sod"] >= 130 and
            d["pot"] <= 5
        ):
            prediction = 0

# 🤖 Otherwise use model
        else:
            prediction = 1 if proba > 0.6 else 0

        confidence = proba * 100

# Advice
        if prediction == 1:
            advice = "⚠️ Visit Doctor"
        else:
            advice = "✅ You are Safe"

        return jsonify({
            "prediction": int(prediction),
            "label": "Kidney Disease Detected" if prediction == 1 else "No Kidney Disease",
            "confidence": round(confidence, 1),
            "advice": advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5100))
    app.run(host="0.0.0.0", port=port, debug=True)