import pandas as pd
import os
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

from model_layer.data.features import add_derivative_feature

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

input_path = os.path.join(BASE_DIR, "data", "processed", "measurements_labeled.csv")
model_path = os.path.join(BASE_DIR, "models", "regime_classifier", "model.pkl")

print("INPUT PATH:", input_path)
print("MODEL PATH:", model_path)

os.makedirs(os.path.dirname(model_path), exist_ok=True)

# ======================
# 1. CARREGAR DADOS
# ======================
df = pd.read_csv(input_path)

# Add derivada no treinamento:
df = add_derivative_feature(df)

# ======================
# 2. FEATURES E TARGET
# ======================
X = df[[
    "tempo",
    "altura",
    "dC_dt"  # {entender que dC_dt = C(t)-C(t-1)} Essa derivada faz com que o modelo entenda não só onde está, mas para onde nestá indo.
]]

y = df["regime"]

# ======================
# 3. SPLIT
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ======================
# 4. MODELO
# ======================
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ======================
# 5. AVALIAÇÃO
# ======================
y_pred = model.predict(X_test)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))

print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))


# Salvar matriz de confusão:
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm)
cm_path = os.path.join(
    BASE_DIR,
    "models",
    "regime_classifier",
    "confusion_matrix.csv"
)
cm_df.to_csv(cm_path, index=False)

# Salvar classification reports
report = classification_report(y_test, y_pred, output_dict=True)

report_path = os.path.join(
    BASE_DIR,
    "models",
    "regime_classifier",
    "metrics.json"
)

with open(report_path, "w") as f:
    json.dump(report, f, indent=4)


# ======================
# 6. SALVAR MODELO
# ======================
joblib.dump(model, model_path)

print(f"\nModelo salvo em: {model_path}")
