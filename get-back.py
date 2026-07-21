import sage_data_client

df = sage_data_client.query(
    start="-30m",
    filter={
        "plugin": ".*plugin-iio.*",
        "name": "upload",
    },
)

print(df[["timestamp", "value"]])