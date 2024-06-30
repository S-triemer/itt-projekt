<template>
    <div>
      <button @click="addRoom">Add Room</button>
      <div class="grid">
        <Room
          v-for="(room, index) in rooms"
          :key="index"
          :room-name="room.name"
          :desired-temperature="room.desiredTemperature"
        />
      </div>
    </div>
  </template>
  
  <script>
import Room from '../components/Room.vue';
import axios from 'axios';

export default {
  components: {
    Room,
  },
  data() {
    return {
      rooms: [],
    };
  },
  methods: {
    addRoom() {
      const roomName = prompt('Enter room name:');
      const desiredTemperature = prompt('Enter desired temperature:');
      const location = prompt('Enter location:');
      if (roomName && desiredTemperature && location) {
        // Keine seperate location für jeden Ort
        this.location = location
        this.rooms.push({
          name: roomName,
          desiredTemperature: desiredTemperature,
        });
        this.updateInfluxDb();
      }
    },
    async updateInfluxDb() {
      await this.getTempForLocation();
      const data = {
        outsideTemp: this.outsideTemp,
        dataPoints: this.rooms.map(room => ({
          room: room.name,
          desiredTemp: parseFloat(room.desiredTemperature)
        }))
      };

      try {
        const response = await axios.post('http://127.0.0.1:5000/generateData', data);
        console.log('Data successfully sent:', response.data);
      } catch (error) {
        console.error('Error sending data:', error);
      }
    },
    async getTempForLocation() {
      const apiKey = '4efb9499402be7968e09dfd915b1e167';
      const url = `http://api.openweathermap.org/data/2.5/weather?q=${this.location}&appid=${apiKey}&units=metric`;
      
      try {
        const response = await axios.get(url);
        this.outsideTemp = response.data.main.temp;
        this.error = ''; 
        console.log('Outside temperature:', this.outsideTemp);
      } catch (err) {
        this.error = 'Error retrieving data';
        this.temperature = null;
      }
    }
  }
};
</script>

  
  <style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
  }
  </style>
  