import pandas as pd
from dagster import (
    AssetCheckResult,
    AssetCheckSpec,
    DataVersion,
    Output,
    asset,
    observable_source_asset,
)

from ..resources import GirderConnection


@observable_source_asset
def input_spreadsheet(girder: GirderConnection):
    fobj = girder.get_file_from_item("PLACEHOLDER")
    return DataVersion(fobj["sha512"])


@asset(
    code_version="v1",
    deps=[input_spreadsheet],
    check_specs=[AssetCheckSpec(name="no_NaNs", asset="versioned_spreadsheet")],
)
def versioned_spreadsheet(girder: GirderConnection) -> Output[pd.DataFrame]:
    fobj = girder.get_file_from_item("PLACEHOLDER")
    df = pd.read_csv(girder.get_stream(fobj["itemId"]))
    yield Output(df, data_version=DataVersion(fobj["sha512"]))

    # check it
    yield AssetCheckResult(
        passed=not df.isna().any().any(),
    )
