import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from flask import Flask, request, jsonify
from flask_cors import CORS
from influxdb_client.client.write_api import SYNCHRONOUS
from Influxdb import InfluxDB
from Configuration import Configuration
import threading
from RoomManager import RoomManager

app = Flask(__name__)
CORS(app)
#Erstelle ein Konfiguration Objekt (Erhält alle notwendigen Konfigurationen der Anwendung)
configuration = Configuration()

# Erstelle eine InfluxDB-Clientinstanz
influxdb = InfluxDB(configuration.url, configuration.token, configuration.org)

room_manager = RoomManager(influxdb, configuration.bucket, configuration.org)

@app.route('/window', methods=['POST'])
def handle_window_event():
    data = request.json
    print(data)
    status = data.get('status')
    room = data.get('room')
    response, status_code = room_manager.handle_window_event(status, room)
    return jsonify(response), status_code
  
@app.route('/generateData', methods=['POST'])
def handle_generate_data():
    print(request.json)
    data = request.json
    data_points = data["dataPoints"]
    room_manager.set_outside_temp(data["outsideTemp"])
    room_manager.start_generating_data(data_points)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(port=5000))
    flask_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")