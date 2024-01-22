from datetime import datetime
import threading
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
          "GLCD",
          "DPIR",
          "RPIR",
          "BRGB"]

ALARM_SYSTEM_IS_ACTIVE = False
ALARM_IS_ON = False
VALID_PIN = "1234#"
PEOPLE_INSIDE = 0

ALARM_CLOCK_TIME = time.time()
ALARM_CLOCK_IS_ON = False
ALARM_CLOCK_SYSTEM_IS_ON = False


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
    elif topic == "DPIR":
        process_dpir(payload)
    elif topic == "RPIR":
        process_rpir(payload)
    elif topic == "BRGB":
        process_brgb(payload)
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
    # print(data)
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


def process_dpir(payload):
    global PEOPLE_INSIDE
    if payload['distance_diff'] >= 0:
        if PEOPLE_INSIDE > 0:
            PEOPLE_INSIDE -= 1
    else:
        PEOPLE_INSIDE += 1
    socketio.emit('message', {'topic': 'people-inside', 'message': {'people_inside': PEOPLE_INSIDE}},
                  room='people-inside')
    print(PEOPLE_INSIDE)


def process_brgb(payload):
    print(payload)
    socketio.emit('message', {'topic': "BRGB", 'message': payload}, room="BRGB")


def process_rpir(payload):
    global PEOPLE_INSIDE, ALARM_SYSTEM_IS_ACTIVE, ALARM_IS_ON
    if PEOPLE_INSIDE == 0:
        if ALARM_SYSTEM_IS_ACTIVE and not ALARM_IS_ON:
            turn_on_alarm(payload["device_id"])


def check_alarm_clock():
    global ALARM_CLOCK_IS_ON
    while True:
        current_time = f"{str(datetime.now().hour)}:{str(datetime.now().minute)}"
        if ALARM_CLOCK_SYSTEM_IS_ON and current_time == ALARM_CLOCK_TIME:
            ALARM_CLOCK_IS_ON = True
            publish.single("alarm-clock",
                           json.dumps({"is_on": True}),
                           hostname=mqtt_host,
                           port=mqtt_port)
        time.sleep(60)


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


@app.route('/dus', methods=['post'])
def dus():
    payload = request.get_json()
    publish.single("DUS-scenario",
                   json.dumps({"device_id": payload["device_id"], "scenario": payload["scenario"]}),
                   hostname=mqtt_host,
                   port=mqtt_port)
    return json.dumps("")


@app.route('/rpir', methods=['post'])
def rpir():
    payload = request.get_json()
    publish.single("RPIR-scenario",
                   json.dumps({"device_id": payload["device_id"]}),
                   hostname=mqtt_host,
                   port=mqtt_port)
    return json.dumps("")


@app.route('/alarm-clock', methods=['post'])
def alarm_clock():
    global ALARM_CLOCK_TIME, ALARM_CLOCK_SYSTEM_IS_ON, ALARM_CLOCK_IS_ON
    payload = request.get_json()
    command = payload["command"]
    if command == "setup":
        alarm_clock_timestamp = datetime.fromtimestamp(payload["alarm_clock_timestamp"])
        ALARM_CLOCK_TIME = f"{str(alarm_clock_timestamp.hour)}:{str(alarm_clock_timestamp.minute)}"
        print(ALARM_CLOCK_TIME)
    elif command == "system":
        ALARM_CLOCK_SYSTEM_IS_ON = payload["is_on"]
    else:
        ALARM_CLOCK_IS_ON = False
        publish.single("alarm-clock",
                       json.dumps({"is_on": False}),
                       hostname=mqtt_host,
                       port=mqtt_port)

    return json.dumps("")


@app.route('/rgb-control', methods=['post'])
def rgb_control():
    payload = request.get_json()
    command = payload["command"]
    publish.single(topic="rgb-control",
                   payload=json.dumps({"command": command}),
                   hostname=mqtt_host,
                   port=mqtt_port)
    return json.dumps("")


if __name__ == '__main__':
    alarm_clock_thread = threading.Thread(target=check_alarm_clock)
    alarm_clock_thread.start()
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
