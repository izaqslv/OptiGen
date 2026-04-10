from model_layer.regimes.regime_rules import (
    smooth_signal,
    compute_derivative,
    classify_regime_point,
    enforce_temporal_consistency
)
from model_layer.regimes.regime_config import REGIME_CONFIG
import pandas as pd

def label_regimes(df):
    #   limpar index problemático
    # df = df.copy()
    # df = df.reset_index(drop=True)

    # aplicar por grupo físico
    df = (
        df.groupby(["fluid_id", "altura"], group_keys=False).apply(process_group)
        #.reset_index(drop=True)
    )

    return df


def process_group(df):
    df = smooth_signal(df)
    df = compute_derivative(df)

    # classificação inicial
    df["regime_raw"] = df.apply(
        lambda row: classify_regime_point(row, REGIME_CONFIG),
        axis=1
    )
    # refinamento temporal
    df = enforce_temporal_consistency(df)
    df["regime"] = df["regime_raw"]

    return df
