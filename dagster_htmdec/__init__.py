import warnings

from dagster import (
    Definitions,
    EnvVar,
    ExperimentalWarning,
    FilesystemIOManager,
)
from dagster._core.definitions.external_asset import (
    create_external_asset_from_source_asset,
)

warnings.filterwarnings("ignore", category=ExperimentalWarning)  # noqa: E402
from .assets import pdv_sources, processed_pdv_data  # noqa: E402
from .jobs import pdv_job  # noqa: E402
from .partitions import pdv_partition  # noqa: E402
from .resources import GirderConnection, GirderCredentials  # noqa: E402
from .resources.io_manager import ConfigurableGirderIOManager  # noqa: E402
from .sensors import make_girder_folder_sensor  # noqa: E402

defs = Definitions(
    assets=[
        create_external_asset_from_source_asset(pdv_sources),
        processed_pdv_data,
    ],
    jobs=[pdv_job],
    sensors=[
        make_girder_folder_sensor(
            pdv_job,
            EnvVar("DATAFLOW_SRC_FOLDER_ID").get_value(),
            "pdv_watchdog",
            pdv_partition,
        )
    ],
    resources={
        "fs_io_manager": FilesystemIOManager(),
        "girder_io_manager": ConfigurableGirderIOManager(
            token=EnvVar("GIRDER_TOKEN"),
            api_url=EnvVar("GIRDER_API_URL"),
            source_folder_id=EnvVar("DATAFLOW_SRC_FOLDER_ID"),
            target_folder_id=EnvVar("DATAFLOW_DST_FOLDER_ID"),
        ),
        "girder": GirderConnection(
            credentials=GirderCredentials(
                token=EnvVar("GIRDER_TOKEN"), api_url=EnvVar("GIRDER_API_URL")
            )
        ),
    },
)
