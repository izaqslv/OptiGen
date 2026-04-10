import pandas as pd

def add_derivative_feature(df):
    """
    Adiciona a derivada dC/dt ao dataframe.
    Agrupa por fluido e altura para manter coerência física.
    """

    df = df.sort_values(by=["fluid_id", "altura", "tempo"])

    df["dC_dt"] = (
        df.groupby(["fluid_id", "altura"])["concentracao"]
        .diff()
        .fillna(0)
    )

    return df
