from flask import Flask
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from communication_credentials import *
from simulators.settings.settings import load_settings

app = Flask(__name__)
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


@app.route('/get-devices', methods=['get'])
def get_devices():
    settings = load_settings("../simulators/settings/settings.json")
    response_settings = []
    for key, value in settings.items():
        value['id'] = key
        response_settings.append(value)

    return json.dumps(response_settings)


if __name__ == '__main__':
    app.run(debug=False)
