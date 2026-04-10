import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import joblib

from business_layer.sedimentation.data_preparation import build_training_dataset


def train_model():

    print("  Carregando dados...")

    # caminho do seu Excel
    file_path = "data/DadosSedimentation.xlsx"

    df_meta = pd.read_excel(file_path, sheet_name="fluids_meta")
    df_measurements = pd.read_excel(file_path, sheet_name="measurements")

    # montar dataset
    X, y = build_training_dataset(df_meta, df_measurements)

    print(f"Shape X: {X.shape}")
    print(f"Shape y: {y.shape}")

    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # normalização
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # modelo
    model = MLPRegressor(
        hidden_layer_sizes=(64, 64),
        activation="relu",
        max_iter=500
    )

    print("  Treinando modelo...")
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"  R² no teste: {score:.4f}")

    # salvar
    joblib.dump(model, "business_layer/sedimentation/model.pkl")
    joblib.dump(scaler, "business_layer/sedimentation/scaler.pkl")

    print("  Modelo salvo com sucesso!")


if __name__ == "__main__":
    train_model()
