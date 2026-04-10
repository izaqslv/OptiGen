# import pandas as pd
# from model_layer.pipeline.data_pipeline import load_and_merge_data
# from model_layer.regimes.regime_labeler import label_regimes
#
# df = load_and_merge_data()
#
# df = label_regimes(df)
#
# print(df[["tempo", "altura", "concentracao", "dC_dt", "regime"]].head(20))

import pandas as pd
from model_layer.regimes.regime_labeler import label_regimes

# carregar dataset direto (SEM pipeline)
df = pd.read_csv("model_layer/data/processed/dataset.csv")

# aplicar labeler
df = label_regimes(df)

# visualizar
print(df[["tempo", "altura", "concentracao", "dc_dt", "regime"]].head(20))