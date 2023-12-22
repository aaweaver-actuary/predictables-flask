from typing import List

import pandas as pd

from .get_json_chunk_filename import get_json_chunk_filename


def dataframe_to_json_chunks(
    df: pd.DataFrame,
    n_chunks: int = 20,
    write_json: bool = True,
    dataset_name: str = None,
) -> List[str]:
    """
    Splits the dataframe into n_chunks of JSON strings.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame to split.
    n_chunks : int, optional
        The number of chunks to split the dataframe into. Default is 20.
    write_json : bool, optional
        A flag indicating whether to write the JSON strings to disk. Default is True.
    dataset_name : str, optional
        The name of the dataset. Default is None, which will result in the JSON files being named 'chunk_001_of_020.json', 'chunk_002_of_020.json', etc.

    Returns
    -------
    json_chunks : list of str
        A list of length `n_chunks` containing the JSON strings for each chunk.
    """
    # Handle dataset_name
    if dataset_name is None:
        dataset_name = "chunk"

    # Ensure n_chunks is not greater than the number of rows in the dataframe
    n_chunks = min(n_chunks, len(df))

    # Check if the JSON files already exist
    if _check_if_json_exists_already(dataset_name, n_chunks):
        print(
            f"JSON files for dataset {dataset_name} already exist. Skipping conversion to JSON."
        )
        return

    # Calculate the size of each chunk
    chunk_size = len(df) // n_chunks

    # Split the dataframe into chunks
    chunks = [df.iloc[i : i + chunk_size] for i in range(0, len(df), chunk_size)]

    # Ensure all data is included in chunks (handling remainder if df size not evenly divisible)
    if len(chunks) > n_chunks:
        last_chunk = chunks[-2].append(chunks[-1])
        chunks = chunks[:-2] + [last_chunk]

    # Convert each chunk to a JSON string and store it in a list
    json_chunks = [chunk.to_json(orient="records") for chunk in chunks]

    # Write the JSON strings to disk
    if write_json:
        for i, chunk in enumerate(json_chunks):
            filename = get_json_chunk_filename(dataset_name, i, n_chunks)
            with open(filename, "w") as f:
                f.write(chunk)

    return json_chunks


def _check_if_json_exists_already(dataset_name: str, n_chunks: int) -> bool:
    """
    Check if the JSON files already exist.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset.
    n_chunks : int
        The total number of chunks.

    Returns
    -------
    bool
        A flag indicating whether the JSON files already exist.
    """
    import os

    # Get the filenames
    filenames = [
        get_json_chunk_filename(dataset_name, i, n_chunks)
        for i in range(1, n_chunks + 1)
    ]

    # Check if the files exist
    return all([os.path.exists(filename) for filename in filenames])
