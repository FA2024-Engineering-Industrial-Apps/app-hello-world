
### 1. Without Data Communication

#### 1.1 Clock Display

##### Input Prompt
I want you to act like an industrial edge application developer who can build an industrial edge application for various specific tasks the user provides.
I will give you some examples and instructions on how to build an IE app.
The file structure should be as follows

```
project
│
└───IE Flow Creator Flows
│   │   flow_data_gen.json
│   
└───mqtt_broker_mosquitto
│   │   .env
│   │   docker-compose.yml
│   
└───node_red
│   │   .env
│   │   docker-compose.yml
│   └───node-red
│   │   │   Dockerfile
│   │   │   flows.json
│   │   │   flows_cred.json
│   │   │   package.json
│   │   │   settings.js
│   
└───my_edge_app
│   │   .env
│   │   docker-compose.yml
│	│   docker-compose_Edge.yml
│   │
│   └───data-analytics
│   │   │   Dockerfile
│   │   │   requirements.txt
│   │   │ 
│	│	└───program
│   │   │   │    app.py
│   │   │   │    data_analytics.py   
│   │
│   └───influxDB
│       │   drive_kpi_calc_dashboard.json
│       │   
```

You need to modify the files in the folder `my_edge_app/program` to realize some of the tasks' functions and return ALL the files inside the whole project (not just files in `my_edge_app/program`!!) as a zip file after generating the code. Remember, other file contents cannot be changed.

Your first task is to build an Edge App that displays the current time full screen. 
Given: Functional requirement: Display time 
Needed: 
- Generate HTML/CSS/JavaScript Code to display the current time and put it into the folder `my_edge_app/program` 
- Package the whole project as IE App and return the package as `clock.zip`.

##### Example Dialogue

[link](https://chatgpt.com/share/0c455914-1f80-4824-b26f-d7b17384ec0a)

Returned package structure
![[img/clock_display.png]]

### 2 With Data Communication (in progress...)

#### 2.1 Pick and Place Machine

##### Input Prompt

I want you to act as an industrial edge application developer who can build an industrial edge application for various specific tasks the user provides.
I will give you some examples and instructions on how to build an IE app.
A typical file structure of an IE app is as follows:
```
project
│
└───IE Flow Creator Flows
│   │   flow_data_gen.json
│   
└───mqtt_broker_mosquitto
│   │   .env
│   │   docker-compose.yml
│   
└───node_red
│   │   .env
│   │   docker-compose.yml
│   └───node-red
│   │   │   Dockerfile
│   │   │   flows.json
│   │   │   flows_cred.json
│   │   │   package.json
│   │   │   settings.js
│   
└───my_edge_app
│   │   .env
│   │   docker-compose.yml
│	│   docker-compose_Edge.yml
│   │
│   └───data-analytics
│   │   │   Dockerfile
│   │   │   requirements.txt
│   │   │ 
│	│	└───program
│   │   │   │    app.py
│   │   │   │    data_analytics.py   
│   │
│   └───influxDB
│       │   drive_kpi_calc_dashboard.json
│       │   
```

REMEMBER, you can only modify the files in the folder `my_edge_app/program` or add some files and folders to realize some of the tasks' functions. Remember, **other file contents** cannot be changed. As a result, you should return ALL the files inside the whole project (not just files in `my_edge_app/program`!!) as a zip file after generating the code.

Your first task is to build a pick-and-place machine that uses materials from different material rolls. This IE app should keep track of the current number of transistors, capacitors, and resistors.

The file structure of the IE app you create should be as follows:
```
project
│
└───IE Flow Creator Flows
│   │   flow_data_gen.json
│   
└───mqtt_broker_mosquitto
│   │   .env
│   │   docker-compose.yml
│   
└───node_red
│   │   .env
│   │   docker-compose.yml
│   └───node-red
│   │   │   Dockerfile
│   │   │   flows.json
│   │   │   flows_cred.json
│   │   │   package.json
│   │   │   settings.js
│   
└───my_edge_app
│   │   .env
│   │   docker-compose.yml
│	│   docker-compose_Edge.yml
│   │
│   └───data-analytics
│   │   │   Dockerfile
│   │   │   requirements.txt
│   │   │ 
│	│	└───program
│   │   │   │    app.py
│   │   │   │    data_analytics.py   
│   │
│   └───influxDB
│       │   drive_kpi_calc_dashboard.json
│       
└───pick_and_place_machine
│   │   .env
│   │   docker-compose.yml
│   │
│   └───machine_test_double
│   │   │   Dockerfile
│   │   │   requirements.txt
│   │   │ 
│	│	└───src
│   │   │   │    main.py
│   │   │   │    machine.py   
│   │   │   │    materialroll.py   
│   │   │   │   


```

That means you should add a folder called `pick_and_place_machine`.
Inside the folder pick_and_place_machine, you should create a`docker-compose.yml` file, a hidden`.env` file, and a subfolder `machine_test_double`.

The `docker-compose.yml` should be as follows
```Dockerfile
version: '2.4' # docker-compose version is set to 2.4

services:

###### PICK-AND-PLACE-MACHINE ######
pick-and-place-machine:
	build:
		context: ./machine_test_double
		args:
			BASE_IMAGE: $BASE_IMAGE #
			http_proxy: $http_proxy # Proxy url's from environment
			https_proxy: $https_proxy
	container_name: pick-and-place-machine
	mem_limit: 350m
	restart: no
	environment: # Environment variables available at container run-time
		http_proxy: $http_proxy # Proxy url's from environment
		https_proxy: $https_proxy
	logging: # allow logging
		options: # we use best pactice here as limiting file size and rolling mechanism
			max-size: "10m" # File size is 10MB
			max-file: "2" # only 2 files created before rolling mechanism applies
	networks: # define networks connected to container 'data-analytics'
	proxy-redirect: # Name of the network

###### NETWORK CONFIG ######
networks: # Network interface configuration
	proxy-redirect: # Reference 'proxy-redirect' as predefined network
		external:
			name: proxy-redirect
		driver: bridge

###### VOLUMES ######
volumes: # Volumes for containers
	db-backup:
```

The `.env` specifies the InfluxDB version and the proxy:
```
BASE_IMAGE=python:3.9.2-alpine3.13
INFLUXDB_VERSION=2.4-alpine
INFLUXDB_DB=edgedb
INFLUXDB_DATA_INDEX_VERSION=tsi1
http_proxy=""
https_proxy=""
no_proxy=localhost,127.0.0.1
```

Inside the folder `machine_test_double`, you should include a `Dockerfile`, a `requirements.txt` and a folder `src` that stores all the source code, i.e., `materialroll.py`, `machine.py`, and `main.py`.

The `Dockerfile` specifies how to build the image of the pick and place machine container. 
```
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN adduser -S nonroot
# install all requirements from requirements.txt
COPY requirements.txt /
RUN pip install -r /requirements.txt; rm -f /requirements.txt

# Set the working directory to /app
WORKDIR /app

# Copy the current dir into the container at /app
COPY ./src/* /app/ 
USER nonroot

# Run app.py when the container launches
CMD ["python", "-u", "-m", "main"]
```

The `requirements.txt` specifies the version of `paho-mqtt`:
```
paho-mqtt==1.5.0
```

Now, I want you to complete the files in `src` based on the functionality description for each file in `src`. You should implement all the functionalities.

1. `materialroll.py`
This file defines a class `MaterialRoll` that models a roll of material used in the pick-and-place machine. 
- **Attributes:**
  - `_material`: The type of material the roll contains (e.g., Transistor, Resistor).
  - `_capacity`: The total number of units in the roll when it's full.
  - `_materials_left`: Tracks how many units are left in the roll.
- **Methods:**
  - `__init__(material, capacity)`: Initializes the material type and capacity.
  - `get_material()`: Retrieves one unit of material from the roll if available, reducing the available amount by one. Returns the material's name or `None` if the roll is empty.
  - `is_empty()`: Checks whether the material roll is empty.

2. `machine.py`
This file defines a class `PickAndPlaceMachine`, which represents the automated machine handling material rolls.
- **Attributes:**
  - `name`: Name of the machine.
  - `_materials`: A dictionary storing material names with their corresponding `MaterialRoll` instances.
  - `_running`: Boolean flag indicating if the machine is running.
- **Methods:**
  - `__init__(name, materials)`: Initializes the machine with a name and a list of materials (each associated with a `MaterialRoll`).
  - `start()`: Starts the machine, continuously processing materials and checking their availability.
  - `shutdown()`: Stops the machine when it's no longer needed or when a material roll is empty.
  - Event handlers for material consumption (`_material_used_event_handler`) and when a material roll becomes empty (`_material_roll_empty_event_handler`).
The machine continuously picks materials from rolls and triggers events when materials are used or when a roll is depleted.

3. `main.py`
This file serves as the main execution script for the machine. It connects the machine to an MQTT broker to send messages about material consumption and handle events like material roll depletion.
- **Attributes:**
  - MQTT client parameters such as broker address, port, username, and password.
- **Methods/Functions:**
  - `on_connect()`, `on_disconnect()`, `on_subscribe()`: Event handlers for connecting, disconnecting, and subscribing to the MQTT broker.
  - `send_material_used_msg(material_name, components_used)`: Sends a message to the MQTT broker whenever materials are consumed.
  - `on_roll_empty(material_name)`: Shuts down the machine if a material roll is empty.
  - `main()`: The main function initializes the machine, sets up MQTT communication, and starts the machine, keeping it running as long as materials are available.
 

##### Example Dialogue

[link](https://chatgpt.com/share/325f7589-e12b-4db0-b0c8-bc313ee61903)

Returned package structure
![[img/pick_and_place_machine.png]]
