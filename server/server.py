from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from communication_credentials import *

app = Flask(__name__)

influxdb_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)

mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_host, mqtt_port, 60)
mqtt_client.loop_start()

# TODO: Add topics as needed
topics = ["Temperature", "Humidity"]


def on_connect(client, userdata, flags, rc):
    for topic in topics:
        client.subscribe(topic)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


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
    write_api.write(bucket=influx_bucket, org=influx_org, record=point)


if __name__ == '__main__':
    app.run(debug=True)
