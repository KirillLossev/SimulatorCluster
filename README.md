# Simulator Cluster

This repo is used to spin up a Docker Compose cluster for simulating the processing of vehicle sensor data using [CARLA](https://carla.org/).

When the cluster is launched, a vehicle will be spawned in CARLA and sensors attached to it. These sensors will push their data to a RabbitMQ instance.

This data can then be used by *Decision Components* to declare some action for the vehicle to take, which are then reported back to the message queue for actuators to execute.

External applications can also connect to the message queue to access data.

A visualizer can be accessed using VNC on `localhost:5900`, or through a web browser on `localhost:5800`. This can also be used to manually control the vehicle.
The primary controls are WASD for movement and Q to shift to reverse.

---

## Requirements
- Docker Engine with the Compose plugin

## Components
The simulated vehicle currently consists of the following scripts:
- `scenario_loader` to arrange the environment for the test
- `drive` for visualization and manual control
- `speed_sensor` to send the vehicle speed as reported by CARLA to the message queue
- `obstacle_sensor` to send distance to an obstacle as reported by CARLA to the message queue
- `obstacle_handling` for determining whether an obstacle is close enough to require braking
- `cruise_control_handling` for determining if acceleration is needed to maintain the set speed
- `control_handling` to aggregate instructions from `obstacle_handling` and `cruise_control_handling` and determine the vehicle's course of action
- `throttle_actuator` to apply the resolved action from `control_handling` to the vehicle

## Feature Interaction Demo
Setting `OBSTACLE_DETECTION_VERSION=1` in `.env` will use a basic heuristic to instruct the vehicle to stop if it detects an obstacle 3m or less in front of it. With the Cruise Control setting at its default value, the vehicle will accelerate but not stop in time to avoid collision with the obstacle.

Upgrading it to `OBSTACLE_DETECTION_VERSION=3` will use an algorithm that adjusts the safe distance based on the vehicle's current speed. In the scenario, it will come to a complete stop before reaching the obstacle.

## Debugging
Containers can be entered with `docker exec -it <container name> bash` to examine any needed files or environment properties.

The RabbitMQ admin panel can be helpful for verifying that components connect to the right queues, send expected messages, or react appropriately to messages. It can be enabled by entering the container and running `rabbitmq-plugins enable rabbitmq_management` and can be accessed at `http://localhost:15672`.
See [RabbitMQ's documentation](https://www.rabbitmq.com/docs/management) for more information.

