# Simulator Cluster

This repo is used to spin up a Docker Compose cluster for simulating the processing of vehicle sensor data using [CARLA](https://carla.org/).

When the cluster is launched, a vehicle will be spawned in CARLA and sensors attached to it. These sensors will push their data to a RabbitMQ instance.

This data can then be used by *Decision Components* to declare some action for the vehicle to take, which are then reported back to the message queue for actuators to execute.

External applications can also connect to the message queue to access data.

# Running the Exemplar

Each component is running in parallel, but the components have a dependency on each other. 
Therefore, the order they are run is important.

## Prerequisites
We have used ``python3.8`` to run our exemplar. 

We have a functioning Carla Simulator on Ubuntu that can be run using the script ``/opt/carla_simulator/CarlaUE4.sh``.

``RabbitMQ`` is also running as a service on the host machine at the default ``localhost:5672``.

With all of these being in place, to run the exemplar one has to first run the Carla Simulation under a ``-RenderOffScreen`` flag. 

## Everything Together
Then run the sensors, *decision components*, and the driving file in the expected order. 
This order can be confusing; therefore, they have been archived in the ``Makefile``.

To run this exemplar, one simply has to run (Given you have the prerequisites):
```
make
```