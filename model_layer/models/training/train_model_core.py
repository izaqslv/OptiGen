import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn.metrics import mean_absolute_error
from model_layer.pipeline.data_pipeline import load_and_merge_data
from model_layer.pipeline.feature_engineering import prepare_features
from model_layer.regimes.regime_labeler import label_regimes

from model_layer.models.core.model_config import FEATURE_COLUMNS, TARGET_COLUMN

# =========================
# 1. LOAD DATA
# =========================
df = load_and_merge_data(
    "model_layer/data/raw/DadosSedimentation.xlsx"
)

# 2. FEATURES ENGINEERING
# add em 09/04/2026
# ========================
# VALIDAÇÃO DE FEATURES
# ========================
df = prepare_features(df)

# 3. LABELS REGIMES
df = label_regimes(df)

# 4. CLEAN
df = df.dropna()

# VALIDAÇÃO
features = FEATURE_COLUMNS
target = TARGET_COLUMN

missing_cols = [col for col in features + [target] if col not in df.columns]

if missing_cols:
    raise ValueError(f"Colunas faltando no dataset: {missing_cols}")

# DEBUG (opcional)
print(df[["concentracao", "dc_dt", "regime", "target"]].head(20))


# =========================
# 2. FEATURES / TARGET
# =========================
# features = [
#     "tempo",
#     "altura",
#     "concentracao",
#     "c_lag1",
#     "c_lag2",
#     "roa",
#     "dens_susp",
#     "dens_solids",
#     "teor_solids",
#     "dp_medio",
#     "m",
#     "n",
#     "dc_dt",
#     "regime"
# ]
#
# target = "target"

# df = df.dropna()



###### BLOCO 1 - MODELO GLOBAL =======================================================================================================
# MODELO GLOBAL (OPCIONAL) para suprir a falta de modelo quando estivermos no modo MODELO POR REGIME lá embaixo!
# ============================================================
# 🔵 PIPELINE 1 — MODELO GLOBAL (BASELINE)
# ============================================================
# Objetivo:
# Treinar um modelo único usando TODOS os dados
#
# Uso:
# - Fallback no predictor
# - Comparação de performance
# - Debug e validação geral
#
# Output:
# model_layer/artifacts/models/model_v1.pkl
# ============================================================
X = df[features]
y = df[target]
print(df.columns)
print(df[["concentracao", "dc_dt", "regime", "target"]].head(20))
# =========================
# 3. SPLIT (SEM SHUFFLE)
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)


# 4. MODELO
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# 5. AVALIAÇÃO
score = model.score(X_test, y_test)
print(f"R2 GLOBAL: {score:.4f}")

# joblib.dump(model, "model_layer/artifacts/models/model_v1.pkl")

# =========================
# 5. AVALIAÇÃO
# =========================
# score = model.score(X_test, y_test)
#
# print(f"R²: {score:.4f}")

# 6. CRIAR PASTAS (segurança) para salvar modelos
os.makedirs("model_layer/artifacts/models", exist_ok=True)
os.makedirs("model_layer/artifacts/metadata", exist_ok=True)
os.makedirs("model_layer/artifacts/metrics", exist_ok=True)

# 7. SALVAR MODELO + FEATURES
joblib.dump(model,"model_layer/artifacts/models/model_v1.pkl")
joblib.dump(features,"model_layer/artifacts/metadata/features_v1.pkl")

# 8. SALVAR MÉTRICAS
metrics = {"r2": float(score), "n_samples": int(len(df))}
with open("model_layer/artifacts/metrics/model_v1_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Modelo, features e métricas salvos com sucesso!")





###### BLOCO 2 - MODELOS POR REGIME =======================================================================================================
# MODELOS POR REGIME: devido à dinâmica altamente não-linear que sofrem impacto pela altura, tempo, derivada, etc!
# ============================================================
# 🟢 PIPELINE 2 — MODELOS ESPECIALIZADOS POR REGIME
# ============================================================
# Objetivo:
# Treinar modelos específicos para cada regime físico
#
# Estratégia:
# - Segmentação via labeler (regime)
# - Um modelo por regime
#
# Uso:
# - Predictor inteligente (seleciona modelo correto)
#
# Output:
# model_layer/models/specialized/model_regime_{i}.pkl
# ============================================================

## ATUALIZAÇÃO: MODELO/TREINO POR REGIME
# def train_models_by_regime(df):
#     base_path = "model_layer/models/specialized"
#     os.makedirs(base_path, exist_ok=True)
#
#     features = [
#         "tempo", "altura", "concentracao",
#         "c_lag1", "c_lag2",
#         "roa", "dens_susp", "dens_solids",
#         "teor_solids", "dp_medio",
#         "m", "n", "dc_dt", "regime"
#     ]
#
#     for regime in [0, 1, 2]:
#
#         df_reg = df[df["regime"] == regime]
#
#         if len(df_reg) == 0:
#             print(f"Regime {regime} sem dados, pulando...")
#             continue
#
#         X = df_reg[features]
#         y = df_reg["target"]
#
#         model = RandomForestRegressor(n_estimators=200, random_state=42)
#         model.fit(X, y)
#
#         #  NOVO: avaliação do modelo
#         preds = model.predict(X)
#         erro = mean_absolute_error(y, preds)
#
#         print(f"Regime {regime} → MAE: {erro:.6f}")
#
#         #  critério inteligente
#         LIMIAR = 0.02  # pode ajustar depois
#
#         if erro > LIMIAR:
#             print(f"Regime {regime} com erro alto ({erro:.6f}), não salvando modelo.")
#             continue
#
#         path = f"{base_path}/model_regime_{regime}.pkl"
#         joblib.dump(model, path)
#
#         print(f"Modelo do regime {regime} salvo em {path}")
#
#     model = RandomForestRegressor(n_estimators=200, random_state=42)
#     model.fit(X, y)
#
#     path = f"{base_path}/model_regime_{regime}.pkl"
#     joblib.dump(model, path)
#
#     print(f"  Modelo do regime {regime} salvo em {path}")

# modificação em 09/04/2026
def train_models_by_regime(df) -> None:
    # from model_layer.models.core.model_config import FEATURE_COLUMNS, TARGET_COLUMN

    base_path = "model_layer/models/specialized"
    os.makedirs(base_path, exist_ok=True)

    features = FEATURE_COLUMNS
    target = TARGET_COLUMN

    for regime in [0, 1, 2]:

        df_reg = df[df["regime"] == regime]

        if len(df_reg) == 0:
            print(f"Regime {regime} sem dados, pulando...")
            continue

        X = df_reg[features]
        y = df_reg[target]

        model = RandomForestRegressor(n_estimators=200, random_state=42)
        model.fit(X, y)

        preds = model.predict(X)
        erro = mean_absolute_error(y, preds)

        print(f"Regime {regime} → MAE: {erro:.6f}")

        LIMIAR = 0.02

        if erro > LIMIAR:
            print(f"Regime {regime} com erro alto ({erro:.6f}), não salvando.")
            continue

        path = f"{base_path}/model_regime_{regime}.pkl"
        joblib.dump(model, path)

        print(f"Modelo do regime {regime} salvo em {path}")


if __name__ == "__main__":
    print("\n🚀 TREINANDO MODELOS POR REGIME...\n")

    train_models_by_regime(df)

