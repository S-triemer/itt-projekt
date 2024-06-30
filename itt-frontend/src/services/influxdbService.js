import { client, org, bucket } from '../influxdb';

const queryApi = client.getQueryApi(org);
export const fetchInfluxData = async (query) => {
    const result = [];
    try {
        const rows = await queryApi.collectRows(query);
        rows.forEach((row) => {
            result.push(row);
        });
    } catch (error) {
        console.error('Error querying InfluxDB:', error);
    }
    return result;
};
