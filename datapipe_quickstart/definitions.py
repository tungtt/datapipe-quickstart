import json
import os

from dagster_duckdb import DuckDBResource
from datapipe_quickstart import assets
from datapipe_quickstart.schedules import weekly_update_schedule
from datapipe_quickstart.sensors import adhoc_request_job, adhoc_request_sensor

import dagster as dg

datapipe_assets = dg.load_assets_from_modules([assets])
datapipe_asset_checks = dg.load_asset_checks_from_modules([assets])

defs = dg.Definitions(
    assets=datapipe_assets,
    asset_checks=datapipe_asset_checks,
    schedules=[weekly_update_schedule],
    jobs=[adhoc_request_job],
    sensors=[adhoc_request_sensor],
    resources={"duckdb": DuckDBResource(database="data/mydb.duckdb")}
)
