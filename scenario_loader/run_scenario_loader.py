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
client.set_timeout(20.0)

if os.environ["MAP"]:
    world = client.load_world(os.environ["MAP"])
else:
    world = client.get_world()

# Set up scenario in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True
world.apply_settings(settings)

hero = carla_util.select_hero_actor(world)
world.tick()

# Spawn another car in front of the hero
SPAWN_DISTANCE = 50 # m

hero_transform = hero.get_transform()
hero_forward_unit = hero_transform.get_forward_vector().make_unit_vector()
partner_spawn = hero_transform
partner_spawn.location.x += SPAWN_DISTANCE * hero_forward_unit.x
partner_spawn.location.y += SPAWN_DISTANCE * hero_forward_unit.y
partner_spawn.location.z += SPAWN_DISTANCE * hero_forward_unit.z
partner_blueprint = carla_util.get_random_blueprint(world)
partner = world.try_spawn_actor(partner_blueprint, partner_spawn)
if partner is None:
    print("Failed to spawn partner!", flush=True)

world.tick()

settings.synchronous_mode = False
world.apply_settings(settings)

# We are done, create the signal file.
with open("loader_done", 'w') as _:
    pass

print("Done!",flush=True)

# Run until stopped
forever = threading.Event()
forever.wait()