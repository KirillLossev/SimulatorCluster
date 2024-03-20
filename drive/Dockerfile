# This container hosts the visualiser and manual controls for the exemplar.
# To avoid trying to spawn a GUI window from inside Docker, an X11 display
# server will run inside the container to be accessed via VNC
FROM jlesage/baseimage-gui:debian-10-v4.5.3 as vnc

# The Python CARLA 1.9.14 package only supports Python 3.8, which is
# not included in the base VNC Debian image. 
# The Debian repos also do not keep old versions of Python around, so
# we can't just install Python 3.8 directly.
# The options are to either build it from source, or to add an existing
# repo that keeps those packages.
# We chose the latter.
RUN apt update && apt install -y ca-certificates

ADD --chmod=655 https://people.debian.org/~paravoid/python-all/unofficial-python-all.asc /etc/apt/trusted.gpg.d/unofficial-python-all.asc 
RUN echo "deb http://people.debian.org/~paravoid/python-all buster main" | tee /etc/apt/sources.list.d/python-all.list

# Python 3.8 and system packages needed to run Pygame
RUN apt update && apt install -y libsdl2-dev fontconfig python3.8

ADD https://bootstrap.pypa.io/get-pip.py get-pip.py
RUN python3.8 get-pip.py

# Install Python dependencies to connect to CARLA, RabbitMQ, and
# present graphics
RUN python3.8 -m pip install pygame numpy pika carla==0.9.14

# Fonts need to be rebuilt for Pygame
RUN fc-cache -f -v

COPY host_util.py carla_util.py drive/run_drive.py /

# The VNC container performs its own setup then invokes /startapp.sh
# to enter our own code
COPY drive/startapp.sh /startapp.sh

RUN chmod +x /startapp.sh

ENV USER_ID=0

RUN set-cont-env APP_NAME "Simulation Viewer"
