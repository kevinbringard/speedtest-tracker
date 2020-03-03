# speedtest-docker
Build a docker container for SpeedTest++ and some tools to track its results

## speedtest-influx.py
Python to spin up the speedtest container and insert the results into an InfluxDB

### Running it
You'll need to create your own influx DB container. You should be able to do something like:
```
docker run -d --name influx -p 8086:8086 -p 2003:2003 -v $( pwd):/var/lib/influxdb influxdb
```

You'll then need to create the database:
```
docker exec -it influx influx
create database speedtest
```

Then you'll need to set the Influx DB info in the python code. Specifically:
```
INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
SPEEDTEST_DB = "speedtest"
```

The above values should work if you're running Influx in a container on your localhost using the default values

You may want to create a virtualenv if you don't want to dirty up your whole system. If you're running python3
you can do:
```
python -m venv --copies --clear venv-influx && source venv-influx/bin/activate
```

Then you'll want to install the requirements:
```
pip install -r requirements.txt
```
