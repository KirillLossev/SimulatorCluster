run_carla = /opt/carla_simulator/CarlaUE4.sh 

python = python3.8

make:
	${run_carla} & sleep 3 &&
		${python} main.py speed_sensor run_speed_sensor.py &
		${python} main.py drive run_drive.py


