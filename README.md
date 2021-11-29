# Homework: Mixture of Communication Pattern
- By Ting-Hao Ling (NTU student ID B07901040)

# Function
- Given the order, find corresponding fibonacci number
- show the search history

# Files
- log.py: MQTT subscriber, collect searching history from MQTT breaker to "log.txt".
- server.py: gRPC servicer, provide both fibonacci calculator and logging service. Notice that the two services come from different communication pattern.
- manage.py: execution of Django server
- /fibonacci/views.py: call the fibonacci servicer by gRPC and publish searching record to MQTT breaker
- /logs/views.py: call the searching history by gRPC


## How to run
- Install project dependencies
```bash
# Install grpc packages
$ pip3 install -r requirements.txt
```
- - Run the backend server
```bash
$ python3 manage.py runserver 0.0.0.0:8000
```

- Start the gRPC service
```bash
$ python3 server.py --ip 0.0.0.0 --port 8080
```

-- Run the eclipse mosquitto docker container
```bash
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

- Run MQTT subscriber
```bash
$ python3 log.py
```

- Ask for fibonacci number
```bash
$ curl -X POST -d "order=[desired order]" http://localhost:8000/rest/fibonacci
```
(replace [desired order] with integer)

- Ask for the searching history
```bash
$ curl -X GET http://localhost:8000/rest/logs
```
