#!/usr/bin/env python

import json

import docker

from influxdb import InfluxDBClient

INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
SPEEDTEST_DB = "speedtest"

docker_client = docker.from_env()
output = docker_client.containers.run("speedtest:latest",
                                       auto_remove=True,
                                       network_mode="host",
                                       command="/speedtest.sh --output json")
output = output.decode("utf-8")
client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
client.switch_database(SPEEDTEST_DB)


def get_influx_json(my_json):
    # Tags first
    isp = my_json['client']['isp']
    ip = my_json['client']['ip']

    # Next the rest of the fields
    lat = my_json['client']['lat']
    lon = my_json['client']['lon']
    servers_online = my_json['servers_online']
    name = my_json['server']['name']
    sponsor = my_json['server']['sponsor']
    distance = my_json['server']['distance']
    latency = my_json['server']['latency']
    host = my_json['server']['host']
    ping = my_json['ping']
    jitter = my_json['jitter']
    download = my_json['download']
    upload = my_json['upload']
    status = my_json['_']

    influx_data = [{
        'measurement': 'speed',
        'tags': {
            'isp': isp,
            'ip': ip
        },
        'fields': {
            'lat': lat,
            'lon': lon,
            'servers_online': int(servers_online),
            'name': name,
            'sponsor': sponsor,
            'distance': distance,
            'latency': int(latency),
            'host': host,
            'ping': int(ping),
            'jitter': int(jitter),
            'download': float(download),
            'upload': float(upload),
            'status': status
        },
    }]

    return influx_data



my_json = json.loads(str(output))
client.write_points(get_influx_json(my_json))
