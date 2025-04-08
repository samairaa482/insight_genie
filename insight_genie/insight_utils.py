import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Load CSV data from a byte stream into a pandas DataFrame.
    
    Args:
        file_bytes (bytes): The raw byte content of the CSV file.
    
    Returns:
        pd.DataFrame: The loaded DataFrame.
    
    Raises:
        ValueError: If the CSV is empty or cannot be parsed.
    """
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        if df.empty:
            raise ValueError("The provided CSV is empty.")
        logger.info("CSV loaded successfully.")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise

def get_basic_stats(df: pd.DataFrame) -> dict:
    """
    Generate basic statistics from the DataFrame.
    
    Args:
        df (pd.DataFrame): Input data.
    
    Returns:
        dict: Basic summary including shape, columns, and descriptive stats.
    """
    if df.empty:
        raise ValueError("Cannot generate stats on an empty DataFrame.")
        
    stats = {
        "shape": df.shape,
        "columns": list(df.columns),
        "summary": df.describe(include='all').to_dict()
    }
    logger.info("Basic statistics generated.")
    return stats

def plot_correlation_heatmap(df: pd.DataFrame) -> bytes:
    """
    Generate a correlation heatmap and return it as bytes.
    
    Args:
        df (pd.DataFrame): Input data.
    
    Returns:
        bytes: PNG image of the correlation heatmap.
    """
    if df.empty:
        raise ValueError("Cannot plot heatmap on an empty DataFrame.")

    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    logger.info("Correlation heatmap generated.")
    return buf.read()
