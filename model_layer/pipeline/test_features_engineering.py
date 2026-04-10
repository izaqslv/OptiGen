from model_layer.pipeline.data_pipeline import load_and_merge_data
from model_layer.pipeline.feature_engineering import prepare_features

df = load_and_merge_data(
    "model_layer/data/raw/DadosSedimentation.xlsx"
)

df_feat = prepare_features(df)

print(df_feat.head())
print("\nColunas finais:")
print(df_feat.columns)


