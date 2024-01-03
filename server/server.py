from flask import Flask
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from communication_credentials import *
from simulators.settings.settings import load_settings
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

influxdb_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)

mqtt_client = mqtt.Client()

# TODO: Add topics as needed
topics = ["Distance",
          "Temperature",
          "Humidity",
          "Door",
          "Passwords",
          "Movement",
          "Acceleration",
          "Rotation",
          "GLCD"]


def on_connect(client, userdata, flags, rc):
    for topic in topics:
        print(topic)
        client.subscribe(topic)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))

mqtt_client.connect(mqtt_host, mqtt_port, 1000)
mqtt_client.loop_start()


def save_to_db(data):
    print(data)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .tag("id", data["id"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=influx_bucket, org=influx_org, record=point)
    socketio.emit('message', {'topic': data["id"], 'message': data}, room=data["id"])


@socketio.on('subscribe')
def handle_subscribe(data):
    topic = data['topic']
    print(f'Client subscribed to topic: {topic}')
    join_room(topic)


@socketio.on('unsubscribe')
def handle_unsubscribe(data):
    topic = data['topic']
    print(f'Client unsubscribed from topic: {topic}')
    leave_room(topic)


@socketio.on('send_message')
def handle_send_message(data):
    topic = data['topic']
    message = data['message']
    # print(f'Received message on topic {topic}: {message}')
    socketio.emit('message', {'topic': topic, 'message': message}, room=topic)


@app.route('/get-devices', methods=['get'])
def get_devices():
    settings = load_settings("../simulators/settings/settings.json")
    response_settings = []
    for key, value in settings.items():
        value['id'] = key
        response_settings.append(value)

    return json.dumps(response_settings)


if __name__ == '__main__':
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
