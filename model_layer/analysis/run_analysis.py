from model_layer.models.core.predictor_core import predict
from model_layer.analysis.plot_predictions import plot_by_fluid
from model_layer.pipeline.data_pipeline import load_and_merge_data

df = load_and_merge_data("model_layer/data/raw/DadosSedimentation.xlsx")

df_pred = predict(df)

plot_by_fluid(df_pred)