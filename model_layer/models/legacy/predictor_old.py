import os
import joblib
import pandas as pd

from model_layer.data.features import add_derivative_feature

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# caminhos
classifier_path = os.path.join(BASE_DIR, "models", "regime_classifier", "model.pkl")
specialized_dir = os.path.join(BASE_DIR, "models", "specialized")

# carregar modelos
classifier = joblib.load(classifier_path)

specialized_models = {
    0: joblib.load(os.path.join(specialized_dir, "regime_0.pkl")),
    1: joblib.load(os.path.join(specialized_dir, "regime_1.pkl")),
    2: joblib.load(os.path.join(specialized_dir, "regime_2.pkl")),
}


def predict(df_input):
    """
    df_input: DataFrame com colunas:
    ["tempo", "altura", "concentracao", "fluid_id"]
    """

    # =========================
    # 1. FEATURE ENGINEERING
    # =========================
    df = add_derivative_feature(df_input.copy())

    # =========================
    # 2. CLASSIFICAR REGIME
    # =========================
    X_class = df[["tempo", "altura", "dC_dt"]]
    regimes = classifier.predict(X_class)

    df["regime_pred"] = regimes

    # =========================
    # 3. PREDIÇÃO ESPECIALIZADA
    # =========================
    predictions = []

    for i, row in df.iterrows():

        regime = row["regime_pred"]

        model = specialized_models[regime]

        X_reg = pd.DataFrame([[
            row["tempo"],
            row["altura"],
            row["concentracao"],
            row["dC_dt"]
        ]], columns=["tempo", "altura", "concentracao", "dC_dt"])

        pred = model.predict(X_reg)[0]

        predictions.append(pred)

    df["concentracao_pred"] = predictions

    return df
