import pandas as pd


def get_chunk_count(df: pd.DataFrame) -> int:
    """
    Get the number of chunks to split the dataframe into.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame to split.

    Returns
    -------
    n_chunks : int
        The number of chunks to split the dataframe into.
    """
    # Calculate the number of chunks
    calc_n_chunks = len(df) // 50000 + 1

    return max(20, calc_n_chunks)
