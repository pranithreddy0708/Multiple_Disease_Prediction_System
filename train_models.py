import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

os.makedirs("models", exist_ok=True)

# ── Diabetes ──────────────────────────────────────────
print("Training Diabetes model...")
df = pd.read_csv("datasets/diabetes.csv")
print("  Columns:", df.columns.tolist())

X, y = df.drop("Outcome", axis=1), df["Outcome"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = SVC(kernel="rbf", probability=True, C=10, gamma=0.1)
model.fit(X_train, y_train)
print(f"  Accuracy: {accuracy_score(y_test, model.predict(X_test)):.2f}")
joblib.dump(model, "models/diabetes_model.pkl")
joblib.dump(scaler, "models/diabetes_scaler.pkl")

# ── Heart Disease ─────────────────────────────────────
print("Training Heart Disease model...")
df = pd.read_csv("datasets/heart.csv")
print("  Columns:", df.columns.tolist())

# Auto-detect target column
target_col = None
for col in ["target", "output", "Heart Disease", "condition", "num"]:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    target_col = df.columns[-1]  # fallback: last column
    print(f"  ⚠️ Target column not found, using last column: '{target_col}'")
else:
    print(f"  ✅ Target column: '{target_col}'")

# Binarize target if needed (some datasets have 0,1,2,3,4)
df[target_col] = (df[target_col] > 0).astype(int)

X, y = df.drop(target_col, axis=1), df[target_col]

# Drop any non-numeric columns
X = X.select_dtypes(include=[np.number])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=10)
model.fit(X_train, y_train)
print(f"  Accuracy: {accuracy_score(y_test, model.predict(X_test)):.2f}")
joblib.dump(model, "models/heart_disease_model.pkl")
joblib.dump(scaler, "models/heart_scaler.pkl")

# ── Parkinson's ───────────────────────────────────────
print("Training Parkinson's model...")
df = pd.read_csv("datasets/parkinsons.csv")
print("  Columns:", df.columns.tolist())

# Drop 'name' only if it exists
drop_cols = ["status"]
if "name" in df.columns:
    drop_cols.append("name")

X = df.drop(drop_cols, axis=1)
y = df["status"]

# Drop any remaining non-numeric columns
X = X.select_dtypes(include=[np.number])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = SVC(kernel="rbf", probability=True, C=10, gamma=0.1)
model.fit(X_train, y_train)
print(f"  Accuracy: {accuracy_score(y_test, model.predict(X_test)):.2f}")
joblib.dump(model, "models/parkinsons_model.pkl")
joblib.dump(scaler, "models/parkinsons_scaler.pkl")

#lung_cancer
print("Training Lung Cancer model...")

df = pd.read_csv("datasets/lung_cancer.csv")
print("  Columns:", df.columns.tolist())

# Auto-detect target column
target_col = None
for col in ["LUNG_CANCER", "target", "output", "lung_cancer", "result"]:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    target_col = df.columns[-1]
    print(f"  ⚠️ Target column not found, using last column: '{target_col}'")
else:
    print(f"  ✅ Target column: '{target_col}'")

# Convert target to binary
df[target_col] = df[target_col].map({'YES':1, 'NO':0})
X, y = df.drop(target_col, axis=1), df[target_col]

# Remove non-numeric columns
X = X.select_dtypes(include=[np.number])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=10)
model.fit(X_train, y_train)

print(f"  Accuracy: {accuracy_score(y_test, model.predict(X_test)):.2f}")

joblib.dump(model, "models/lung_cancer_model.pkl")
joblib.dump(scaler, "models/lung_scaler.pkl")

#
print("Training Kidney Disease model...")

df = pd.read_csv("datasets/kidney_disease.csv")
print("  Columns:", df.columns.tolist())

# Auto-detect target column
target_col = None
for col in ["classification", "target", "KidneyDisease", "kidney_disease"]:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    target_col = df.columns[-1]
    print(f"  ⚠️ Target column not found, using last column: '{target_col}'")
else:
    print(f"  ✅ Target column: '{target_col}'")

# Convert target to binary
df[target_col] = df[target_col].apply(lambda x: 1 if str(x).lower() in ["ckd", "1", "yes"] else 0)

X, y = df.drop(target_col, axis=1), df[target_col]

# Keep numeric columns only
X = X.select_dtypes(include=[np.number])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=10)
model.fit(X_train, y_train)

print(f"  Accuracy: {accuracy_score(y_test, model.predict(X_test)):.2f}")

joblib.dump(model, "models/kidney_disease_model.pkl")
joblib.dump(scaler, "models/kidney_scaler.pkl")

print("\n✅ All models trained and saved successfully!")