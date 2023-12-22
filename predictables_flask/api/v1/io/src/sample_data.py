import pandas as pd
from flask import jsonify


def get_sample_data(ds_name: str, orient: str = "records") -> str:
    """
    Get data from parquet file represented by ds_name and return it as a json string.
    """
    try:
        return jsonify(
            pd.read_parquet(f"./api/v1/io/data/{ds_name}.parquet").to_json(
                orient=orient
            )
        )
    except Exception as e:
        return jsonify({"error": str(e)})
