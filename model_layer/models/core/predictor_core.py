# ============================================================
# PREDICTOR CORE — OPTIGEN
# ============================================================
# Objetivo:
# Executar inferência usando modelos treinados
#
# Estratégia:
# - Pipeline idêntico ao treino
# - Seleção automática por regime
# - Fallback para modelo global
#
# Entrada:
# DataFrame com colunas definidas em model_config
#
# Saída:
# DataFrame com coluna 'concentracao_pred'
# ============================================================

import joblib
import pandas as pd
from model_layer.pipeline.feature_engineering import prepare_features
from model_layer.regimes.regime_labeler import label_regimes
import os

from model_layer.models.core.model_config import (FEATURE_COLUMNS, TARGET_COLUMN, MODEL_PATHS)


# CARREGAR MODELO
def load_models():
    models = {}

    # modelos por regime
    for regime, path in MODEL_PATHS["regime"].items():
        if os.path.exists(path):
            models[regime] = joblib.load(path)
        else:
            print(f"[WARN] Modelo regime {regime} não encontrado")

    # modelo global
    global_path = MODEL_PATHS["global"]

    global_model = None
    if os.path.exists(global_path):
        global_model = joblib.load(global_path)
    else:
        print("[WARN] Modelo global não encontrado")

    return models, global_model


# VALIDATE INPUT
def validate_input(df: pd.DataFrame):
    required_cols = FEATURE_COLUMNS

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Colunas faltando no input: {missing}")

# PREDICT
def predict(df_input: pd.DataFrame) -> pd.DataFrame:
    # 1. cópia
    df = df_input.copy()

    # 2. pipeline (igual treino: gera features faltantes)
    df = prepare_features(df)
    df = label_regimes(df)

    # 3. validação ("Validação deve ocorrer no estágio onde os dados já estão no formato esperado pelo modelo.")
    validate_input(df)

    # 4. limpeza
    df = df.dropna()

    # 5. carregar modelos
    models, global_model = load_models()

    # 6. features
    X = df[FEATURE_COLUMNS]

    preds = []

    for i, row in X.iterrows():

        regime = int(df.loc[i, "regime"])
        model = models.get(regime)

        # fallback inteligente
        if model is None:
            if global_model is not None:
                model = global_model
            else:
                preds.append(None)
                continue

        pred = model.predict(pd.DataFrame([row.values], columns=FEATURE_COLUMNS))[0]
        # preds.append(pred)
        preds.append(float(pred))

    df["concentracao_pred"] = preds

    # DEBUG: remover depois de validar (reaultado tem que ser 2124 2124 (correto), se for 0 2124 (errado)
    # print(len(preds), len(df))

    return df
