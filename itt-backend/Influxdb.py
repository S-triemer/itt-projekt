from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDB:
    def __init__(self, url, token, org):
        self.client = InfluxDBClient(url=url, token=token, org=org);
        self.influxdbwriter = self.client.write_api(write_options=SYNCHRONOUS)
