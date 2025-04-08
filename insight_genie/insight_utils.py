import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def load_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes))

def get_basic_stats(df: pd.DataFrame) -> dict:
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "summary": df.describe(include='all').to_dict()
    }

def plot_correlation_heatmap(df: pd.DataFrame) -> bytes:
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()
