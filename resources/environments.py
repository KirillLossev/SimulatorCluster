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

debug_info = []
if env_vars["CC_SPEED"]:
    debug_info.append("Cruise Control Setting: " + env_vars["CC_SPEED"] + " km/h")