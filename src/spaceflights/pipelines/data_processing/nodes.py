"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.0.0
"""
import pandas as pd

def _is_true(x: pd.Series) -> pd.Series:
    return x == "t"

def _parse_percentage(x: pd.Series) -> pd.Series:
    return x.str.replace("%","").astype(float)

def _parse_price(x: pd.Series) -> pd.Series:
    return x.str.replace("$","").str.replace(",","").astype(float)

def preprocess_companies(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the companies dataset.

    Args:
        companies: Raw companies dataframe.

    Returns:
        Preprocessed companies dataframe.
    """
    df['iata_approved'] = _is_true(df['iata_approved'])
    df['company_rating'] = _parse_percentage(df['company_rating'])
    return df

def preprocess_shuttles(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the shuttles dataset.

    Args:
        shuttles: Raw shuttles dataframe.

    Returns:
        Preprocessed shuttles dataframe.
    """
    df['d_check_complete'] = _is_true(df['d_check_complete'])
    df['moon_clearance_complete'] = _is_true(df['moon_clearance_complete'])
    df['price'] = _parse_price(df['price'])
    return df

def create_model_input_table(
    shuttles: pd.DataFrame,
    companies: pd.DataFrame,
    reviews: pd.DataFrame
) -> pd.DataFrame:
    rated_shuttles = shuttles.merge(reviews, left_on="id", right_on="shuttle_id")
    model_input_table = rated_shuttles.merge(companies,left_on="company_id", right_on="id")
    return model_input_table.dropna()

