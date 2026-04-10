import pandas as pd
from pathlib import Path


def load_excel_data(excel_path: str):
    """
    Carrega as abas do Excel.
    """
    df_meta = pd.read_excel(excel_path, sheet_name="fluids_meta")
    df_meas = pd.read_excel(excel_path, sheet_name="measurements")

    return df_meta, df_meas


def standardize_columns(df: pd.DataFrame):
    """
    Padroniza nomes das colunas.
    """
    df.columns = df.columns.str.lower().str.strip()
    return df


def merge_data(df_meta: pd.DataFrame, df_meas: pd.DataFrame):
    """
    Faz merge entre measurements e fluids_meta.
    """
    if "fluid_id" not in df_meta.columns or "fluid_id" not in df_meas.columns:
        raise ValueError("Coluna 'fluid_id' não encontrada em uma das tabelas.")

    df = df_meas.merge(df_meta, on="fluid_id", how="left")

    return df


def save_processed_data(df: pd.DataFrame, output_path: str):
    """
    Salva dataset processado (CSV).
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def load_and_merge_data(excel_path: str, save_path: str = None):
    """
    Pipeline completo:
    - lê Excel
    - padroniza colunas
    - faz merge
    - opcionalmente salva CSV
    """

    # 🔹 Carregar
    df_meta, df_meas = load_excel_data(excel_path)

    # 🔹 Padronizar
    df_meta = standardize_columns(df_meta)
    df_meas = standardize_columns(df_meas)

    # 🔹 Merge
    df = merge_data(df_meta, df_meas)

    # 🔹 Salvar (opcional)
    if save_path:
        save_processed_data(df, save_path)

    return df 