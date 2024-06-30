import { InfluxDB } from '@influxdata/influxdb-client';

const url = 'http://localhost:8086';
const token = 'my-token';
const org = 'my-org';
const bucket = 'my-bucket';

const client = new InfluxDB({ url, token });

export { client, org, bucket };
