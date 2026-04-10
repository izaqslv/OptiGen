from model_layer.pipeline.data_pipeline import load_and_merge_data

df = load_and_merge_data(
    "model_layer/data/raw/DadosSedimentation.xlsx",
    save_path="model_layer/data/processed/dataset.csv"
)

print(df.head())
print("\nColunas:")
print(df.columns)