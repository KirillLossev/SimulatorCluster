run_carla = /opt/carla_simulator/CarlaUE4.sh 

python = python3.8

make:
	${run_carla} -nosound -RenderOffScreen &
	sleep 5
	${python} speed_sensor/run_speed_sensor.py & 
	${python} drive/run_drive.py

kill:
	pgrep -f ${run_carla} | kill



