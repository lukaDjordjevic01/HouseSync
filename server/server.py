import time

from flask import Flask, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

from paho.mqtt import publish

from communication_credentials import *
from simulators.settings.settings import load_settings
from flask_socketio import SocketIO, join_room, leave_room, send
from simulators.alarm.alarm import *

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

ALARM_SYSTEM_IS_ACTIVE = False
ALARM_IS_ON = False
VALID_PIN = "1234#"


def on_connect(client, userdata, flags, rc):
    for topic in topics:
        print(topic)
        client.subscribe(topic)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: process_message(msg)

mqtt_client.connect(mqtt_host, mqtt_port, 1000)
mqtt_client.loop_start()


def process_message(msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    topic = msg.topic
    if topic == "Alarm":
        process_alarm(payload)
    elif topic == "Passwords":
        process_pin(payload)
        save_to_db(payload)
    elif topic == "Door":
        process_door(payload)
        save_to_db(payload)
    else:
        save_to_db(payload)


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .tag("id", data["id"])
        .field("measurement", data["value"])
    )
    print(data)
    write_api.write(bucket=influx_bucket, org=influx_org, record=point)
    socketio.emit('message', {'topic': data["id"], 'message': data}, room=data["id"])


def process_pin(payload):
    global ALARM_SYSTEM_IS_ACTIVE
    if ALARM_SYSTEM_IS_ACTIVE and VALID_PIN == payload['value']:
        turn_off_alarm(payload["id"])
        publish.single("Alarm", json.dumps({"command": "deactivate"}), hostname=mqtt_host, port=mqtt_port)
        ALARM_SYSTEM_IS_ACTIVE = False
    elif ALARM_SYSTEM_IS_ACTIVE and VALID_PIN != payload['value']:
        turn_on_alarm(payload["id"])
    elif not ALARM_SYSTEM_IS_ACTIVE and VALID_PIN == payload['value']:
        time.sleep(10)
        publish.single("Alarm", json.dumps({"command": "activate"}), hostname=mqtt_host, port=mqtt_port)
        ALARM_SYSTEM_IS_ACTIVE = True
        print("Aktiviran alarm")
    elif not ALARM_SYSTEM_IS_ACTIVE and VALID_PIN != payload['value']:
        print("Dobio sa weba!!!")


def process_alarm(payload):
    command = payload['command']
    if command == 'notify':
        socketio.emit('message', {'topic': "Alarm", 'message': payload['message']}, room="Alarm")
    elif command == 'on' or command == 'off':
        global ALARM_IS_ON
        ALARM_IS_ON = command == 'on'
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        point = (
            Point("Alarm")
            .tag("device_id", payload['device_id'])
            .field("command", payload['command'])
        )
        write_api.write(bucket=influx_bucket, org=influx_org, record=point)


def process_door(payload):
    global ALARM_SYSTEM_IS_ACTIVE, ALARM_IS_ON
    locked = payload['value']
    if not locked:
        print("Uso")
        time.sleep(5)
        if ALARM_SYSTEM_IS_ACTIVE and not ALARM_IS_ON:
            turn_on_alarm(payload["id"])


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


@app.route('/dms-pin', methods=['post'])
def dms_pin():
    payload = request.get_json()
    publish.single("DMS", json.dumps({"scenario": payload["scenario"]}), hostname=mqtt_host, port=mqtt_port)
    return json.dumps("")


@app.route('/ds', methods=['post'])
def ds():
    payload = request.get_json()
    publish.single("DS", json.dumps({"device_id": payload["device_id"]}), hostname=mqtt_host, port=mqtt_port)
    return json.dumps("")


if __name__ == '__main__':
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
