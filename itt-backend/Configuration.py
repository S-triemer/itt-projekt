class Configuration:
    def __init__(self):
        # Verbindungsdetails zum Influxdb Container
        self.url = "http://localhost:8086"
        self.token = 'my-token'
        self.org = "my-org"
        self.bucket = "my-bucket"