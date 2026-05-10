import os, json, joblib
import pandas as pd
from model_layer2.dataset.dataset_builder_v3 import build_dataset_v3
from model_layer2.inference_fun.v3_engine import run_autoregressive_loop

# Resolução de caminhos absolutos para evitar erros no Render
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts"))
RUNS_DIR = os.path.join(BASE_DIR, "runs")
MODELS_DIR = os.path.join(BASE_DIR, "models")
CONFIG_DIR = os.path.join(BASE_DIR, "config")


# Carregamento seguro dos artefatos
def load_artifacts():
    with open(os.path.join(RUNS_DIR, "last_run.json")) as f:
        paths = json.load(f)
    model = joblib.load(os.path.join(MODELS_DIR, paths["model"]))
    with open(os.path.join(CONFIG_DIR, paths["features"])) as f:
        features = json.load(f)
    return model, features


model, FEATURES = load_artifacts()


def predict_concentration_v3(measurements, fluids_meta):
    df = build_dataset_v3(measurements, fluids_meta)
    df = df.sort_values(["fluid_id", "altura", "tempo"]).reset_index(drop=True)

    out = []
    for (fid, h), g in df.groupby(["fluid_id", "altura"]):
        g = g.sort_values("tempo").reset_index(drop=True)

        # Executa a lógica centralizada
        g["pred_concentracao"] = run_autoregressive_loop(
            model=model,
            features_list=FEATURES,
            group_df=g,
            initial_concentration=g.loc[0, "concentracao"]
        )
        out.append(g)

    return pd.concat(out).reset_index(drop=True)
