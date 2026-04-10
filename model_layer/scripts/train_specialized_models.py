import pandas as pd
import os
import joblib

from sklearn.ensemble import RandomForestRegressor

from model_layer.data.features import add_derivative_feature

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

input_path = os.path.join(BASE_DIR, "data", "processed", "measurements_labeled.csv")
models_dir = os.path.join(BASE_DIR, "models", "specialized")

os.makedirs(models_dir, exist_ok=True)

print("INPUT PATH:", input_path)
print("MODELS DIR:", models_dir)

# =========================
# 1. CARREGAR DADOS
# =========================
df = pd.read_csv(input_path)

# =========================
# 2. FEATURES
# =========================
df = add_derivative_feature(df)

# =========================
# 3. LOOP POR REGIME
# =========================
for regime in df["regime"].unique():

    print(f"\n=== Treinando modelo para regime {regime} ===")

    df_regime = df[df["regime"] == regime]

    #  FEATURES
    X = df_regime[
        [
            "tempo",
            "altura",
            "concentracao",
            "dC_dt"
        ]
    ]

    #  TARGET (aqui você pode evoluir depois)
    y = df_regime["concentracao"]

    # =========================
    # MODELO
    # =========================
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )

    model.fit(X, y)

    # =========================
    # SALVAR
    # =========================
    model_path = os.path.join(models_dir, f"regime_{regime}.pkl")

    joblib.dump(model, model_path)

    print(f"Modelo salvo em: {model_path}")
