import math
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
          "BRGB",
          "B4SD",
          "Alarm"]

ALARM_SYSTEM_IS_ACTIVE = False
ALARM_IS_ON = False
VALID_PIN = "1234#"
PEOPLE_INSIDE = 0

ALARM_CLOCK_TIME = "Not set"
ALARM_CLOCK_IS_ON = False
ALARM_CLOCK_SYSTEM_IS_ON = False
ALARM_CLOCK_PAYLOAD = {"time": ALARM_CLOCK_TIME, "system_is_on": ALARM_CLOCK_SYSTEM_IS_ON}

BGRB_PAYLOAD = {"color": "white", "is_on": False}

B4SD_TIME = ""


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
    elif topic == "B4SD":
        process_b4sd(payload)
    elif topic == "Acceleration":
        process_acceleration(payload)
    elif topic == "GLCD":
        process_glcd(payload)
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
        socketio.emit('message',
                      {'topic': 'alarm-system-activation', 'message': {'alarm_system_is_active': False}},
                      room='alarm-system-activation')
    elif ALARM_SYSTEM_IS_ACTIVE and VALID_PIN != payload['value']:
        turn_on_alarm(payload["id"])
    elif not ALARM_SYSTEM_IS_ACTIVE and VALID_PIN == payload['value']:
        time.sleep(10)
        publish.single("Alarm", json.dumps({"command": "activate"}), hostname=mqtt_host, port=mqtt_port)
        ALARM_SYSTEM_IS_ACTIVE = True
        socketio.emit('message',
                      {'topic': 'alarm-system-activation', 'message': {'alarm_system_is_active': True}},
                      room='alarm-system-activation')
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
        if ALARM_SYSTEM_IS_ACTIVE:
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
    global BGRB_PAYLOAD
    print(payload)
    BGRB_PAYLOAD = payload
    socketio.emit('message', {'topic': "BRGB", 'message': payload}, room="BRGB")


def process_b4sd(payload):
    global B4SD_TIME
    B4SD_TIME = payload['time']
    socketio.emit('message', {'topic': "B4SD", 'message': payload}, room="B4SD")


def process_rpir(payload):
    global PEOPLE_INSIDE, ALARM_SYSTEM_IS_ACTIVE, ALARM_IS_ON
    if PEOPLE_INSIDE == 0:
        if ALARM_SYSTEM_IS_ACTIVE:
            turn_on_alarm(payload["device_id"])


def process_acceleration(payload):
    global ALARM_SYSTEM_IS_ACTIVE, ALARM_IS_ON
    save_to_db(payload)
    ax, ay, az = payload['value'].split()
    magnitude = math.sqrt(float(ax) ** 2 + float(ay) ** 2)
    if magnitude > 3 and ALARM_SYSTEM_IS_ACTIVE:
        turn_on_alarm(payload["id"])


def process_glcd(payload):
    socketio.emit('message', {'topic': "GLCD", 'message': payload}, room="GLCD")


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


def alarm_clock_notify():
    global ALARM_CLOCK_IS_ON
    while True:
        if ALARM_CLOCK_IS_ON:
            socketio.emit('message', {'topic': "Alarm-clock", 'message': {"is_on": True}}, room="Alarm-clock")
        time.sleep(3)


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
    global ALARM_CLOCK_TIME, ALARM_CLOCK_SYSTEM_IS_ON, ALARM_CLOCK_IS_ON, ALARM_CLOCK_PAYLOAD
    payload = request.get_json()
    command = payload["command"]
    if command == "setup":
        alarm_clock_timestamp = datetime.fromtimestamp(payload["alarm_clock_timestamp"] / 1000)
        hour = str(alarm_clock_timestamp.hour)
        if len(hour) == 1:
            hour = "0" + hour
        minute = str(alarm_clock_timestamp.minute)
        if len(minute) == 1:
            minute = "0" + minute
        ALARM_CLOCK_TIME = f"{hour}:{minute}"
        ALARM_CLOCK_PAYLOAD["time"] = ALARM_CLOCK_TIME
        print(ALARM_CLOCK_TIME)
    elif command == "system":
        ALARM_CLOCK_SYSTEM_IS_ON = payload["is_on"]
        ALARM_CLOCK_PAYLOAD["system_is_on"] = ALARM_CLOCK_SYSTEM_IS_ON
    else:
        ALARM_CLOCK_IS_ON = False
        publish.single("alarm-clock",
                       json.dumps({"is_on": False}),
                       hostname=mqtt_host,
                       port=mqtt_port)
    return json.dumps(ALARM_CLOCK_PAYLOAD)


@app.route('/rgb-control', methods=['post'])
def rgb_control():
    payload = request.get_json()
    command = payload["command"]
    publish.single(topic="rgb-control",
                   payload=json.dumps({"command": command}),
                   hostname=mqtt_host,
                   port=mqtt_port)
    return json.dumps("")


@app.route('/rgb-state', methods=['get'])
def rgb_state():
    return json.dumps(BGRB_PAYLOAD)


@app.route('/acceleration', methods=['post'])
def acceleration():
    publish.single(topic="GSG-scenario",
                   payload=json.dumps({"command": "acceleration"}),
                   hostname=mqtt_host,
                   port=mqtt_port)
    return json.dumps("")


@app.route('/people-inside', methods=['GET'])
def people_inside():
    return json.dumps({"people_inside": PEOPLE_INSIDE})


@app.route('/alarm-system-is-active', methods=['GET'])
def alarm_system_is_active():
    return json.dumps({"alarm_system_is_active": ALARM_SYSTEM_IS_ACTIVE})


@app.route('/web-alarm-off', methods=['post'])
def web_alarm_off():
    payload = request.get_json()
    if payload["value"] != VALID_PIN:
        return json.dumps({"message": "Invalid pin!"}), 400
    process_pin(payload)
    return json.dumps("")


@app.route('/get-time', methods=['get'])
def get_time():
    global B4SD_TIME
    return json.dumps({"time": B4SD_TIME})


@app.route('/get-alarm-clock', methods=['get'])
def get_alarm_clock():
    global ALARM_CLOCK_PAYLOAD, ALARM_CLOCK_TIME, ALARM_CLOCK_SYSTEM_IS_ON
    ALARM_CLOCK_PAYLOAD["time"] = ALARM_CLOCK_TIME
    ALARM_CLOCK_PAYLOAD["system_is_on"] = ALARM_CLOCK_SYSTEM_IS_ON
    return json.dumps(ALARM_CLOCK_PAYLOAD)


if __name__ == '__main__':
    alarm_clock_thread = threading.Thread(target=check_alarm_clock)
    alarm_clock_thread.start()
    alarm_clock_notify_thread = threading.Thread(target=alarm_clock_notify)
    alarm_clock_notify_thread.start()
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
