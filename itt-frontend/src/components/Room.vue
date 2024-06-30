<template>
    <div class="room">
      <div class="room-name">{{ roomName }}</div>
      <div class="temperature">Desired Temperature: {{ desiredTemperature }}°C</div>
      <div class="actual-temperature">Actual Temperature: {{ latestTemperature }}°C</div>
      <button @click="toggleWindow">{{ windowOpen ? 'Close Window' : 'Open Window' }}</button>
    </div>
  </template>
  
  <script>
  import { fetchInfluxData } from '../services/influxdbService';
  import axios from 'axios';
  export default {
    props: {
      roomName: {
        type: String,
        required: true,
      },
      desiredTemperature: {
        type: String,
        required: true,
      }
    },
    data() {
      return {
        latestTemperature: null,
        windowOpen: false
      };
    },
    methods: {
      async updateTemperature() {
        const data = await fetchInfluxData(this.query);
        console.log(data);  
        if (data) {
          this.latestTemperature = parseFloat(data[0]._value.toFixed(1));
          console.log(this.latestTemperature);
        }
        this.loading = false;
      },
      async toggleWindow() {
        console.log("toggleWindow");
        this.windowOpen = !this.windowOpen; // Toggle window state
        const status = this.windowOpen ? 'open' : 'closed';
        try {
          await axios.post('http://127.0.0.1:5000/window', {
            status: status,
            room: this.roomName
          });
          console.log(`Window ${status} successfully.`);
        } catch (error) {
          console.error('Error toggling window:', error);
        }
    },
    },
    created() {
      this.query = `from(bucket: "my-bucket")
                |> range(start: -10m)
                |> filter(fn: (r) => r._measurement == "home")
                |> filter(fn: (r) => r._field == "temp")
                |> filter(fn: (r) => r.room == "${this.roomName}")
                |> sort(columns: ["_time"], desc: true)
                |> limit(n: 1)`;
      this.updateTemperature();
      this.intervalId = setInterval(this.updateTemperature, 1000);
    },
  };
  </script>
  
  <style>
  .room {
    border: 1px solid #ccc;
    padding: 20px;
    text-align: center;
    background-color: #181818;
  }
  .room-name {
    font-size: 1.5em;
    margin-bottom: 10px;
  }
  .temperature {
    font-size: 1em;
    color: #555;
  }
  </style>
  