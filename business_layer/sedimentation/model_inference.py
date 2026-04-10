import joblib
import numpy as np

# carregar modelo e scaler (uma vez só)
model = joblib.load("business_layer/sedimentation/model.pkl")
scaler = joblib.load("business_layer/sedimentation/scaler.pkl")


#---- FUNÇÃO PARA GERAR PONTO DE PREDIÇÃO:
def predict_concentration(data: dict):

    # ordem EXATA das features (IMPORTANTÍSSIMO)
    features = [
        data["tempo"],
        data["altura"],
        data["ROA"],
        data["dens_susp"],
        data["dens_solids"],
        data["teor_solids"],
        data["dp_medio"],
        data["m"],
        data["n"]
    ]

    X = np.array(features).reshape(1, -1)

    # normalizar
    X_scaled = scaler.transform(X)

    # prever
    prediction = model.predict(X_scaled)

    return float(prediction[0])


#---- FUNÇÃO PARA GERAR CURVAS DE PREDIÇÃO:
def predict_curve(base_data: dict, tempos: list):

    results = []

    for t in tempos:
        data = base_data.copy()
        data["tempo"] = t

        pred = predict_concentration(data)
        results.append(pred)

    return {
        "tempo": tempos,
        "concentracao": results
    }


## (05/04/2026) FUNÇÃO PARA COMPARAÇÃO: RN vs dado experimentais
def compare_with_experimental(base_data: dict, tempos: list, y_exp: list) -> dict:
    result = predict_curve(base_data, tempos)

    y_pred = np.array(result["concentracao"])
    y_exp = np.array(y_exp)

    #  Métricas
    mae = np.mean(np.abs(y_pred - y_exp))
    rmse = np.sqrt(np.mean((y_pred - y_exp) ** 2))

    # R²
    ss_res = np.sum((y_exp - y_pred) ** 2)
    ss_tot = np.sum((y_exp - np.mean(y_exp)) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    # erro por ponto
    erro_ponto = list(np.abs(y_pred - y_exp))

    return {
        "tempo": tempos,
        "predito": list(y_pred),
        "experimental": list(y_exp),
        "erro_ponto": erro_ponto,
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2)
    }
