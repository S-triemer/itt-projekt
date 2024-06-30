<template>
    <div>
        <h1>InfluxDB Data</h1>
        <div v-if="loading">Loading...</div>
        <div v-else>
            <pre>{{ data }}</pre>
        </div>
    </div>
</template>

<script>
import { fetchInfluxData } from '../services/influxdbService';

export default {
    data() {
        return {
            data: [],
            loading: true,
        };
    },
    async created() {
        const query = `from(bucket: "my-bucket")
                  |> range(start: -10m)
                  |> filter(fn: (r) => r._measurement == "home")
                  |> filter(fn: (r) => r._field == "temp")
                  |> filter(fn: (r) => r.room == "Kitchen")
                  |> sort(columns: ["_time"], desc: true)
                  |> limit(n: 1)`;
        this.data = await fetchInfluxData(query);
        this.loading = false;
    },
};
</script>
