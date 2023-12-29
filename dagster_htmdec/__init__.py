import warnings

from dagster import (
    Definitions,
    EnvVar,
    ExperimentalWarning,
    FilesystemIOManager,
)

warnings.filterwarnings("ignore", category=ExperimentalWarning)  # noqa: E402
from .assets import (  # noqa: E402
    input_spreadsheet,
    versioned_spreadsheet,
)
from .resources import GirderConnection, GirderCredentials  # noqa: E402

defs = Definitions(
    assets=[
        input_spreadsheet,
        versioned_spreadsheet,
    ],
    resources={
        "fs_io_manager": FilesystemIOManager(),
        "girder": GirderConnection(
            credentials=GirderCredentials(
                token=EnvVar("GIRDER_TOKEN"), api_url=EnvVar("GIRDER_API_URL")
            )
        ),
    },
)
