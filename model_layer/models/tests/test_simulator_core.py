import pandas as pd
from model_layer.models.core.simulator_core import simulate


def run_test():
    df = pd.read_csv("model_layer/data/processed/dataset.csv")

    # pegar um fluido específico
    df = df[df["fluid_id"] == df["fluid_id"].iloc[0]]

    # pehgar tempo específico
    df_initial = df[df["tempo"] == df["tempo"].min()].copy()

    # inicializar lags
    df_initial["c_lag1"] = df_initial["concentracao"]
    df_initial["c_lag2"] = df_initial["concentracao"]

    required_cols = [
        "tempo", "altura", "concentracao",
        "roa", "dens_susp", "dens_solids",
        "teor_solids", "dp_medio",
        "m", "n", "adensante"
    ]

    for col in required_cols:
        if col not in df_initial.columns:
            raise ValueError(f"Coluna faltando no df_initial: {col}")

    df_sim = simulate(df_initial, steps=10, dt=1.0)

    print(df_sim.head())
    print(df_sim.tail())


if __name__ == "__main__":
    run_test()
