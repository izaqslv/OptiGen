import pandas as pd

from model_layer.models.core.predictor_core import predict


def simulate(C0, altura, tempos):
    """
    Simula a evolução da concentração ao longo do tempo.

    Parâmetros:
    - C0: concentração inicial
    - altura: altura fixa
    - tempos: lista ou array de tempos (ex: [1,2,3,...])

    Retorna:
    - DataFrame com evolução temporal
    """

    resultados = []

    prev_c = C0
    prev_prev_c = C0

    for i, t in enumerate(tempos):

        if i == 0:
            dC_dt = 0

        else:
            dt = tempos[i] - tempos[i - 1]

            if dt == 0:
                dC_dt = 0
            else:
                dC_dt = (prev_c - prev_prev_c) / dt

        df_input = pd.DataFrame([{
            "tempo": t,
            "altura": altura,
            "concentracao": prev_c,
            "fluid_id": 0,  # placeholder
            "dC_dt": dC_dt  # será recalculado também, mas ajuda
        }])

        result = predict(df_input)

        pred_c = result["concentracao_pred"].iloc[0]
        regime = result["regime_pred"].iloc[0]

        resultados.append({
            "tempo": t,
            "altura": altura,
            "concentracao": pred_c,
            "regime": regime
        })

        prev_prev_c = prev_c
        prev_c = pred_c

    return pd.DataFrame(resultados)
