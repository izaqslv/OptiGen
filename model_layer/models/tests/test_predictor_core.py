import pandas as pd
from model_layer.models.core.predictor_core import predict

# Testando...
if __name__ == "__main__":
    from model_layer.pipeline.data_pipeline import load_and_merge_data

    df = load_and_merge_data("model_layer/data/raw/DadosSedimentation.xlsx")

    df_pred = predict(df)

    print(df_pred[["regime", "concentracao", "concentracao_pred"]].head(30))

# carregar seus dados (os mesmos do treino, por enquanto)
df = pd.read_csv("model_layer/data/processed/dataset.csv")

# rodar predição
df_pred = predict(df)

# calcular erro
df_pred["erro"] = df_pred["concentracao_pred"] - df_pred["concentracao"]
df_pred["erro_abs"] = df_pred["erro"].abs()

print("\n Estatísticas do erro:")
print(df_pred["erro_abs"].describe())

print("\n Piores previsões:")
print(df_pred.sort_values("erro_abs", ascending=False).head(10))

## Classificar por regime:
for regime in sorted(df_pred["regime"].unique()):
    df_r = df_pred[df_pred["regime"] == regime]

    print(f"\n--- Regime {regime} ---")
    print(df_r["erro_abs"].describe())



# # OPCIONAL: visualizar os dados experimentais e testar o modelo na predição
# from model_layer.analysis.plot_predictions import plot_by_fluid
#
# df_pred = predict(df)
#
# plot_by_fluid(df_pred)