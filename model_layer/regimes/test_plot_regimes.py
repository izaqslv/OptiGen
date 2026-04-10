import matplotlib.pyplot as plt

from model_layer.pipeline.data_pipeline import load_and_merge_data
from model_layer.regimes.regime_labeler import label_regimes


# =========================
# 1. Carregar dados
# =========================
excel_path = "model_layer/data/raw/DadosSedimentation.xlsx"  # <-- ajuste aqui

df = load_and_merge_data(excel_path)


# =========================
# 2. Aplicar regimes
# =========================
df = label_regimes(df)


# =========================
# 3. Escolher fluido e altura
# =========================
fluid_id = 10
altura = 2

df_plot = df[
    (df["fluid_id"] == fluid_id) &
    (df["altura"] == altura)
]


# =========================
# 4. Plot
# =========================
plt.figure(figsize=(10, 6))

plt.plot(
    df_plot["tempo"],
    df_plot["concentracao"],
    color="black",
    linewidth=2,
    label="Concentração"
)

for regime, color, label in [
    (0, "green", "Regime 0 - Estável"),
    (1, "orange", "Regime 1 - Transição"),
    (2, "red", "Regime 2 - Sedimentação")
]:
    subset = df_plot[df_plot["regime"] == regime]

    plt.scatter(
        subset["tempo"],
        subset["concentracao"],
        color=color,
        label=label,
        s=60
    )

plt.xlabel("Tempo")
plt.ylabel("Concentração")
plt.title(f"Regimes - Fluido {fluid_id} | Altura {altura}")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
