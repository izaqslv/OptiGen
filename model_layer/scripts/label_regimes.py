import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

input_path = os.path.join(BASE_DIR, "data", "raw", "DadosSedimentation.xlsx")
output_path = os.path.join(BASE_DIR, "data", "processed", "measurements_labeled.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df = pd.read_excel(input_path, sheet_name="measurements")
df = df.sort_values(by=["fluid_id", "altura", "tempo"])

regimes = []

threshold_drop = 0.002
threshold_stable = 0.0005

for (fluid, altura), group in df.groupby(["fluid_id", "altura"]):
    group = group.sort_values("tempo")

    prev_c = None
    prev_t = None

    for _, row in group.iterrows():
        if prev_c is None:
            regimes.append(1)  # neutro inicial
        else:
            dc = row["concentracao"] - prev_c
            dt = row["tempo"] - prev_t
            derivada = dc / dt if dt != 0 else 0

            if derivada < -threshold_drop:
                regimes.append(2)
            elif abs(derivada) < threshold_stable:
                regimes.append(0)
            else:
                regimes.append(1)

        prev_c = row["concentracao"]
        prev_t = row["tempo"]

df["regime"] = regimes

df.to_csv(output_path, index=False)
