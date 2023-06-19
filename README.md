# Simulators

dropper &amp; Paperscents simulators

## prerequisites

1. install python@^3.10 through a virtual environment
2. install poetry with `pip3 install poetry`
3. install docker

## environment setup

1. install project dependencies with `poetry install`
2. setup the mqtt local broker with docker and docker-compose
3. setup the .env file at the project's root [see .env exemple here](##environment variables)

## environment variables

a basic .env exemple

`DROPPER_RUN`: the simulator will generate droppers events when this value is set to `"true"`
`DROPPER_SERIALS`: comma separated list of specifics droppers serials, if an empty list is provided, the simulator will generate 10 serials randomly.
`MQTT_HOST`: the mqtt broker url, if you're running it locally through the provided docker-compose then use `"localhost"`
`MQTT_PORT`: the port on which the mqtt broker runs (usualy `"1883"`).

```bash
DROPPER_RUN="true"
DROPPER_SERIALS=""
MQTT_HOST="localhost"
MQTT_PORT="1883"
```
