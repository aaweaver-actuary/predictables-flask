def get_json_chunk_filename(dataset_name: str, i: int, n_chunks: int) -> str:
    """
    Get the filename for the current chunk.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset.
    i : int
        The index of the current chunk.
    n_chunks : int
        The total number of chunks.

    Returns
    -------
    filename : str
        The filename for the current chunk.
    """
    return f"{dataset_name}_{str(i+1).zfill(3)}_of_{str(n_chunks).zfill(3)}.json"
