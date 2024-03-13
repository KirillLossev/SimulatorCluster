# Simulator Cluster

This repo is used to spin up a Docker Compose cluster for simulating the processing of vehicle sensor data using [CARLA](https://carla.org/).

When the cluster is launched, a vehicle will be spawned in CARLA and sensors attached to it. These sensors will push their data to a RabbitMQ instance.

This data can then be used by *Decision Components* to declare some action for the vehicle to take, which are then reported back to the message queue for actuators to execute.

External applications can also connect to the message queue to access data.

A visualizer can be accessed using VNC on `localhost:5900`, or through a web browser on `localhost:5800`. This can also be used to manually control the vehicle.

---

## Requirements
- Docker Engine with the Compose plugin
