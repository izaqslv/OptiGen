import pandas as pd

def add_derivative(df: pd.DataFrame):
    """
    Calcula dc/dt por fluido e altura (derivada real).
    """

    #  ordenar corretamente
    df = df.sort_values(by=["fluid_id", "altura", "tempo"])

    #  diferença de concentração
    dc = df.groupby(["fluid_id", "altura"])["concentracao"].diff()

    #  diferença de tempo
    dt = df.groupby(["fluid_id", "altura"])["tempo"].diff()

    #  derivada real
    df["dc_dt"] = dc / dt

    #  tratar NaN e infinitos
    df["dc_dt"] = df["dc_dt"].replace([float("inf"), -float("inf")], 0)
    df["dc_dt"] = df["dc_dt"].fillna(0)

    return df



def prepare_features(df: pd.DataFrame):
    """
    Remove colunas desnecessárias e define features finais.
    """
    df = add_derivative(df)
    df = add_lags(df)
    df = create_target(df)

    # df = df.fillna(0)

    # # ❌ remover ID
    # df = df.drop(columns=["fluid_id", "adensante"])

    return df


def create_target(df: pd.DataFrame):
    """
    Cria target como concentração no próximo tempo.
    """

    df = df.sort_values(by=["fluid_id", "altura", "tempo"])

    df["target"] = df.groupby(["fluid_id", "altura"])["concentracao"].shift(-1)

    # remover última linha de cada grupo (não tem target)
    df = df.dropna(subset=["target"])

    return df



def add_lags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona memória temporal (lags) da concentração.
    """

    df = df.sort_values(by=["fluid_id", "altura", "tempo"])

    df["c_lag1"] = df.groupby(["fluid_id", "altura"])["concentracao"].shift(1)
    df["c_lag2"] = df.groupby(["fluid_id", "altura"])["concentracao"].shift(2)

    df["c_lag3"] = df.groupby(["fluid_id", "altura"])["concentracao"].shift(3)
    df["c_lag4"] = df.groupby(["fluid_id", "altura"])["concentracao"].shift(4)

    df["dc_dt"] = df.groupby(["fluid_id", "altura"])["concentracao"].diff()

    return df
