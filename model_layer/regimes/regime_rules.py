# Lógica física


#     Classifica regime com base na derivada da concentração:
#     0 → homogêneo
#     1 → transição
#     2 → sedimentação




# Suavização da concentração (SMOOTHING)
def smooth_signal(df, window=3):
    df = df.copy()
    df["concentracao_smooth"] = (
        df["concentracao"]
        .rolling(window=window, center=True)
        .mean()
    )

    # fallback nas bordas
    df["concentracao_smooth"] = df["concentracao_smooth"].fillna(df["concentracao"])

    return df


## DERIVATIVE
def compute_derivative(df):
    # garantir ordenação temporal
    df = df.sort_values("tempo").copy()

    # calcular delta de tempo (evita divisão por zero)
    dt = df["tempo"].diff().replace(0, 1e-6)

    # derivada da concentração suavizada
    df["dc_dt"] = df["concentracao_smooth"].diff() / dt

    # tratar valores iniciais (NaN da diff)
    df["dc_dt"] = df["dc_dt"].fillna(0)

    return df


# Critério físico de regime (CLASSIFICAÇÃO BASE)
def classify_regime_point(row, config):
    dc_dt = row["dc_dt"]
    c = row["concentracao_smooth"]

    if dc_dt < config["threshold_sedimentation"] and c > config["min_concentration"]:
        return 2  # sedimentação

    elif abs(dc_dt) < config["threshold_stable"]:
        return 0  # estável

    else:
        return 1  # transição



## CONSISTÊNCIA TEMPORAL
def enforce_temporal_consistency(df, window=3):
    regimes = df["regime_raw"].values
    refined = regimes.copy()

    for i in range(len(regimes)):
        start = max(0, i - window + 1)
        window_slice = regimes[start:i+1]

        counts = {
            0: (window_slice == 0).sum(),
            1: (window_slice == 1).sum(),
            2: (window_slice == 2).sum()
        }

        refined[i] = max(counts, key=counts.get)

    df["regime"] = refined
    return df
