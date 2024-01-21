import os
import threading
import carla
import carla_util
from pathlib import Path
from host_util import parse_hostport

print("Starting!", flush=True)

# Other scripts/containers will rely on the scenario having been loaded.
# This script will use the existence of a known file ("loader_done") to signal
# that it has completed. This file will be cleared when this script starts,
# but there is the possibility of a race condition if it is checked before
# being deleted.

Path("loader_done").unlink(missing_ok=True)

if not os.environ["CARLA_SERVER"]:
    print("The address of the CARLA server is not specified. Set the CARLA_SERVER environment variable.")
    exit()

(carla_host, carla_port) = parse_hostport(os.environ["CARLA_SERVER"])
client = carla.Client(carla_host, carla_port)
client.set_timeout(2.0)

if os.environ["MAP"]:
    world = client.load_world(os.environ["MAP"])
else:
    world = client.get_world()

carla_util.spawn_hero(world)

# We are done, create the signal file.
with open("loader_done", 'w') as _:
    pass

print("Done!",flush=True)

# Run until stopped
forever = threading.Event()
forever.wait()