from resources.host_util import parse_hostport
# from resources.carla_util import *

from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')

try:
    env_vars["CARLA_SERVER"]
except KeyError:
    print("The address of the CARLA server is not specified. Set the CARLA_SERVER environment variable.")
    exit()

try:
    env_vars["HUD_VERSION"]
except KeyError:
    print("The HUD component version is not specified. Set the HUD_VERSION environment variable.")
    exit()

try:
    env_vars["MQ_SERVER"]
except KeyError:
    print("The address of the Message Queue server is not specified. Set the MQ_SERVER environment variable.")
    exit()

(carla_host, carla_port) = parse_hostport(env_vars["CARLA_SERVER"])
(mq_host, mq_port) = parse_hostport(env_vars["MQ_SERVER"])
hud_version = env_vars["HUD_VERSION"]

debug_info = []
if env_vars["CC_SPEED"]:
    debug_info.append("Cruise Control Setting: " + env_vars["CC_SPEED"] + " km/h")


# ==============================================================================
# -- Running the file ----------------------------------------------------------
# ==============================================================================

if __name__ == "__main__":
    import sys
    import importlib.util


    # Check if the script was called with the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <folder> <script.py>")
        exit(1)

    module_folder = sys.argv[1]
    module_name = sys.argv[2]
    module_path = f'{module_folder}/{module_name}'

    print(f'##### Importing {module_path} #####')
    
    module_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)