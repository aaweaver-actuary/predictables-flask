from flask import jsonify

from .dataframe_to_json_chunks import dataframe_to_json_chunks
from .get_json_chunk_filename import get_json_chunk_filename


def get_data(dataset_name: str, chunk: int):
    data = {"chunk_number": chunk, "data": "..."}
    return jsonify(data)
