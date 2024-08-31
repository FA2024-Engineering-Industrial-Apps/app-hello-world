
# Hello World App for Siemens Industrial Edge

Welcome to the **Hello World App for Siemens Industrial Edge**! This repository contains a simple yet illustrative example of a scenario involving a pick-and-place machine, which demonstrates the interaction between various components within an industrial environment using Siemens Industrial Edge. 

## Project Overview

This project simulates a pick-and-place machine that uses materials from different material rolls. The communication between different modules is handled via an MQTT bus, where each module operates within its own Docker container. Here’s a brief rundown of the process:

- **Pick and Place Machine**: The machine is designed to send an MQTT message each time it uses up a certain amount of material.
- **Edge App**: This application listens to the messages from the pick-and-place machine, calculates the remaining material, and sends this data back to the MQTT bus.
- **Node-RED**: Node-RED captures the data from the MQTT bus and sends it to an InfluxDB instance.
- **InfluxDB**: InfluxDB stores the data, which is then visualized on a dashboard, providing a real-time overview of the material usage.

This setup showcases how different industrial components can communicate and work together within an edge computing environment, utilizing Siemens Industrial Edge.

## Getting Started

### Prerequisites

Before you can run this project, ensure that you have the following installed:

- **Docker**: Make sure Docker is installed and running on your machine.
- **Docker Compose**: Required to orchestrate the multi-container Docker applications.
- **MQTT Broker**: The project assumes an MQTT broker is available.
- **Node-RED**: Included as part of the Docker setup.
- **InfluxDB**: Included as part of the Docker setup.

### Running the Project

To start the scenario, follow these steps:

1. **Clone the Repository**

   First, clone this repository to your local machine:

   ```bash
   git clone https://github.com/FA2024-Engineering-Industrial-Apps/app-hello-world.git
   cd siemens-industrial-edge-hello-world
   ```

2. **Start the Environment**

   Run the provided script to start up all the necessary Docker containers:

   ```bash
   ./start_environment.sh
   ```

   > **Note:** Depending on your system configuration, you may need to use `sudo` to run Docker commands:

   ```bash
   sudo ./start_environment.sh
   ```

3. **Access the InfluxDB Dashboard**

   Once the containers are up and running, you can log in to the InfluxDB dashboard to monitor the material usage:

   - **URL**: [http://localhost:38086](http://localhost:38086)
   - **Username**: `edge`
   - **Password**: `edgeadmin`

   This dashboard will display the real-time data being sent by Node-RED from the MQTT bus.

## License

This project is licensed under the MIT License.