# Simulator Cluster

This repo is used to spin up a Docker Compose cluster for simulating the processing of vehicle sensor data using [CARLA](https://carla.org/).

When the cluster is launched, a vehicle will be spawned in CARLA and sensors attached to it. These sensors will push their data to a RabbitMQ instance.

This data can then be used by *Decision Components* to declare some action for the vehicle to take, which are then reported back to the message queue for actuators to execute.

External applications can also connect to the message queue to access data.

---

## Requirements
- Docker Engine with the Compose plugin

## Limitations
This cluster is intended to launch a CARLA server as well, however due to issues with graphics drivers in Docker this is not implemented.
A server will have to be run separately, and the `CARLA_HOST` environment variable in `compose.yml` set to its address. (By default, the cluster will attempt to connect on the same machine on the default port 2000)

The spawned vehicle is intended to be controllable through a `pygame` window that it launches, however it does not appear when the cluster runs, even if an X Display Server is running.