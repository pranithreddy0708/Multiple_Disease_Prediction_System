import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib, os

os.makedirs('models', exist_ok=True)
df = pd.read_csv('datasets/heart.csv')

target = df.columns[-1]
X = df.drop(columns=[target])
y = (df[target] > 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_sc, y_train)

joblib.dump(model, 'models/heart_disease_model.pkl')
joblib.dump(scaler, 'models/heart_disease_scaler.pkl')
print('Done!')