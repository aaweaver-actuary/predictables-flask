import pandas as pd
from flask import Blueprint, jsonify, request

io_blueprint = Blueprint("io", __name__)


@io_blueprint.route("/sample-data/<ds_name>", methods=["GET"])
@io_blueprint.route("/sample-data/<ds_name>/<orient>", methods=["GET"])
def sample_data(ds_name, orient="split"):
    from .src.sample_data import get_sample_data

    return get_sample_data(ds_name.replace("-", "_"), orient)


@io_blueprint.route("/data/get-chunk-count/<dataset_name>/<df>", methods=["GET"])
@io_blueprint.route("/data/get-chunk-count/<dataset_name>", methods=["GET"])
def get_n_chunks(dataset_name=None, df=None):
    from .src.get_chunk_count import get_chunk_count
    from .src.sample_data import get_sample_data

    if (
        (df is None and dataset_name is None)
        or (df is None and dataset_name == "")
        or (df == "" and dataset_name == "")
    ):
        return jsonify(
            dataset="none", n_chunks=0, error="No dataset name or dataframe provided"
        )
    elif df is not None and dataset_name is not None:
        return jsonify(dataset=dataset_name, n_chunks=get_chunk_count(df))
    elif df is not None:
        return jsonify(dataset="no_name", n_chunks=get_chunk_count(df))
    else:
        if dataset_name in ["breast-cancer", "california-housing"]:
            dataset_name = dataset_name.replace("-", "_")
            df = get_sample_data(dataset_name).response[0].decode("utf-8")
            df = pd.read_json(df)
            return jsonify(dataset=dataset_name, n_chunks=get_chunk_count(df))
        else:
            return jsonify(
                dataset=dataset_name,
                n_chunks=0,
                error=f"Dataset {dataset_name} was not found",
            )


@io_blueprint.route("/data/chunk-dataset/<dataset_name>/<n_chunks>", methods=["GET"])
def chunk_dataset(dataset_name):
    from .src.dataframe_to_json_chunks import dataframe_to_json_chunks
    from .src.get_chunk_count import get_chunk_count

    n_chunks = get_chunk_count(dataset_name).get("n_chunks")

    # Run the chunking process
    try:
        dataframe_to_json_chunks(dataset_name, n_chunks, write_json=True)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
