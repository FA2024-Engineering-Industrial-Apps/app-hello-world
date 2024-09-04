
### 1. Without Data Communication

##### Prompt
I want you to be an industrial edge application developer who can build an industrial edge application for various specific tasks the user provides.
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

https://chatgpt.com/share/0c455914-1f80-4824-b26f-d7b17384ec0a
Returned package structure
![[img/clock_display.png]]

### 2 With Data Communication (in progress...)

 Various components are necessary for the IE app:
 1. **IE Data bus (MQTT broker)**: distributing data about certain topics that are populated by system apps or custom apps by publishing and subscribing to these topics
2. **OPC UA Connector**: a system app that publishes data on Databus. It receives data from the OPC UA server, which provides data from a PLC. 
3. **SIMATIC Flow Creator**: consuming the data from the OPC UA Connector topics on the Databus. The data is preprocessed in the SIMATIC Flow Creator before being published on the Databus again.
4. **Data Analytics container**: consuming the preprocessed data on the topics from the SIMATIC Flow Creator. Calculations and evaluations are then performed using Python data analytics, and the results are returned as KPIs to the Databus. The data analytics container requires an MQTT client to handle the Databus publishes and subscriptions.
5. The **SIMATIC Flow Creator** consumes the analyzed data again. The SIMATIC Flow Creator persistently stores the (raw) and analyzed data in InfluxDB.
6. **InfluxDB**: a time series database that is optimized for fast, high-availability storage and retrieval of time series data. It stores the data transmitted by the OPC UA server to the app and the analyzed data.  
7. **InfluxDB Dashboards**: basic data visualization.
Let's look at the components one by one.
##### Mosquitto MQTT Broker

All necessary files for the MQTT Broker container are placed in the `mqtt_broker_mosquitto` folder containing a `docker-compose.yml` and a `.env` file.

An example of the `docker-compose.yml`  is as follows. This is preconfigured, which means you shouldn't change the content in principle.
```Dockerfile
### Docker Compose File for MQTT Broker - Replacement of IE Databus ###
# This docker-compose file creates a preconfigured MQTT Broker container without authentication

version: '2.4'                                # docker-compose version is set to 2.4 

services:

    mqtt-broker:
      image: eclipse-mosquitto:$MQTT_VERSION  # define image to pull from docker hub if not already on your machine available
      container_name: ie-databus              # Name of MQTT broker container
      restart: unless-stopped                 # always restarts (see overview page 12 Industrial Edge Developer Guide)
      logging:                                # allow logging
        options:                              # we use best pactice here as limiting file size and rolling mechanism
          max-size: "10m"                     # File size is 10MB
          max-file: "2"                       # only 2 files created before rolling mechanism applies
      volumes:                                # mount volume from host
        - mosquitto:/mosquitto:ro             # set to read-only volume
      ports:                                  # expose of ports and publish
        - "33083:1883"                        # map containers default MQTT port (1883) to host's port 33083
      networks:                               # define networks connected to container 'mqtt-broker' 
        proxy-redirect:                       # Name of the network

###### NETWORK CONFIG ######
networks:                           # Network interface configuration
  proxy-redirect:                   # Reference 'proxy-redirect' as predefined network
    name: proxy-redirect
    driver: bridge

###### VOLUMES ######
volumes:                            # Volumes for containers
  mosquitto:
```

The `.env` specifies the MQTT version and the proxy:

> Please be aware of the variables for the HTTP and HTTPS proxy. You must set them in the .env file. The default value is empty, which means no proxy is used. Please configure your proxy if you use one, e.g., as in most company network environments.

```
MQTT_VERSION=1.6.14
http_proxy=""
https_proxy=""
no_proxy=localhost,127.0.0.1
```

##### Node-RED
The Node-RED replaces the SIMATIC S7 Connector and SIMATIC Flow Creator on the IED. All the required files for the Node-RED container are in the `node_red` folder. It contains a `docker-compose.yml`, `.env` file, and another folder, `node-red`.

The Dockerfile specifies how to build the image of the Node-RED container. 
```Dockerfile
### Docker Compose File for node-red - Replacement of Southbound and SIMATIC Flow Creator ###
# This docker-compose file creates a preconfigured NodeRed container MQTT connection

version: '2.4'                                # docker-compose version is set to 2.4 

services:

  ###### NODE-RED ######
  nodered:
    build:                                    # Configuration applied at build time
      context: ./node-red                     # Relative Path to node-red from this docker-compose file containing Dockerfile
      args:                                   # Args variables available only at build-time
        no_proxy: $no_proxy
        http_proxy: $http_proxy               # Proxy url's from environment
        https_proxy: $https_proxy
    image: nodered:v0.0.1                     # Name of the built image
    container_name: nodered                   # Name of the node-red container
    restart: unless-stopped                   # always restarts (see overview page 12 Industrial Edge Developer Guide)
    environment:                              # Environment variables available at container run-time
      http_proxy: $http_proxy                 # Proxy url's from environment
      https_proxy: $https_proxy
    logging:                                  # allow logging
      options:                                # we use best pactice here as limiting file size and rolling mechanism
        max-size: "10m"                       # File size is 10MB
        max-file: "2"                         # only 2 files created before rolling mechanism applies
    ports:                                    # expose of ports and publish
      - "33080:1880"                          # map containers port 33080 to host's port 1880
    networks:                                 # define networks connected to container 'data-analytics' 
      proxy-redirect:                         # Name of the network
    external_links:                            # Dependencie on other container
      - influxdb                               # Wait for start of container 'influxdb'

####### NETWORK CONFIG ######
networks:                           # Network interface configuration
  proxy-redirect:                   # Reference 'proxy-redirect' as predefined network
    external:                       # Note: Please create the network manually as it is preexisting on Industrial Edge Device
      name: proxy-redirect
    driver: bridge
```

It describes which version of Node-RED is used, which plugins will be loaded, and how to perform configurations such as copying the example workflow.

##### My Edge App

This is the app that will be published to the IEM and deployed on IEDs. All the files required for your first IE app are in the `my_edge_app` folder.

The `my_edge_app` folder contains the following files:
- **docker-compose.yml**: This is the docker-compose.yml to create the containers for the development environment and the image for the Industrial Edge.
- **docker-compose_Edge.yml**: This is the adapted docker-compose.yml file, which will be used later for uploading your first app to the IEM with the IEAP.
- **data-analytics folder**: This folder contains the Python app for doing scientific calculations with the collected and preprocessed data. It also contains the Dockerfile to build the corresponding image.

The Dockerfile builds the data-analytics in the `data_analytics` folder. All Python library dependencies are loaded from `requirements.txt` and added to the base package. It uses a basic Python image from the environment variables in the `.env` file. It copies all Python files from the `program` folder to the container's execution environment and runs `app.py` when the container starts.

The `app.py` calls the main methods of `data_analytics.py`. The `data_analytics.py` contains the scientific calculations and an MQTT client for receiving and sending data.