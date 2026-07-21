"""Query recent measurements and uploads produced by this Sage app."""

import sage_data_client

df = sage_data_client.query(
    start="-30m",
    filter={
        "plugin": ".*my-amazing-app-name.*",
        "name": "color\\.mean\\..*|upload",
    },
)

print(df[["timestamp", "name", "value"]])
