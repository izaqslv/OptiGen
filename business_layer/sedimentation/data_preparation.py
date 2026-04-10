import pandas as pd
import numpy as np

def build_training_dataset(df_meta, df_measurements):

    # merge
    df = df_measurements.merge(df_meta, on="fluid_id")

    # remover coluna categórica
    if "adensante" in df.columns:
        df = df.drop(columns=["adensante"])

    # features
    features = [
        "tempo",
        "altura",
        "ROA",
        "dens_susp",
        "dens_solids",
        "teor_solids",
        "dp_medio",
        "m",
        "n"
    ]

    X = df[features].values
    y = df["concentracao"].values

    return X, y
