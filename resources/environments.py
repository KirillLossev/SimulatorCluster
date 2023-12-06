import urllib.parse

# https://stackoverflow.com/a/53172593
def parse_hostport(hp):
    # urlparse() and urlsplit() insists on absolute URLs starting with "//"
    result = urllib.parse.urlsplit('//' + hp)
    return result.hostname, result.port

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

try:
    env_vars["CC_SPEED"]
except KeyError:
    print("Cruise Control speed is not specified")
    exit()

debug_info = ["Cruise Control Setting: " + env_vars["CC_SPEED"] + " km/h"]
cc_speed = float(os.environ["CC_SPEED"])

try:
    env_vars["VERSION"]
except KeyError:
    print("The component version to run is not specified. Set the VERSION environment variable.")
    exit()

version = env_vars["VERSION"]