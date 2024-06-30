import concurrent.futures
import time
from influxdb_client import Point
from ValueObjects.Temperature import Temperature

class RoomManager:
    def __init__(self, influxdb, bucket, org):
        self.influxdb = influxdb
        self.bucket = bucket
        self.org = org
        self.room_status = {}
        self.room_temperatures = {}
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.outside_temp = 21.0

    def start_generating_data(self, data_points):
        for dp in data_points:
            room = dp['room']
            self.room_status[room] = 'closed'
            self.room_temperatures[room] = Temperature(dp['desiredTemp'])
            self.executor.submit(self.generate_temperature, room) 

    def generate_temperature(self, room):
        while True:
            temp_obj = self.room_temperatures[room]
            
            if self.room_status[room] == 'open':
                temp_obj.reach_outside_temp(self.outside_temp)
            elif self.room_status[room] == 'closed':
                temp_obj.reach_desired_temp()

            point = (
                Point('home')
                .tag('room', room)
                .field('temp', temp_obj.value)
            )
            try:
                self.influxdb.influxdbwriter.write(bucket=self.bucket, org=self.org, record=point)
                print(f"Temperature written to InfluxDB for room: {room}")
            except Exception as e:
                print(f"Error writing to InfluxDB: {e}")
            time.sleep(1)

    def handle_window_event(self, status, room):
        if status not in ['open', 'closed']:
            return {'status': 'error', 'message': 'Invalid status'}, 400
        
        if room not in self.room_temperatures:
            return {'status': 'error', 'message': 'Room not found'}, 404

        self.room_status[room] = status
        return {'status': 'success'}, 200

    def set_outside_temp(self, outside_temp):
        self.outside_temp = outside_temp
        return {'status': 'success'}, 200