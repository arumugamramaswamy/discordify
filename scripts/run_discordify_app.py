import logging
from os.path import splitext
from sys import argv, path
from discordify import config_bot

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
# TODO figure out a way to remove this
path.append(".")

# TODO use argparse
config = argv[1]
_, ext = splitext(config)
ext = ext[1:]
token = argv[2]
print(
    f"Running app... with config type {ext}, config file {config}, token file {token}"
)

if ext == "json":
    bot = config_bot.parse_json(config)
elif ext == "yaml":
    bot = config_bot.parse_yaml(config)

with open(token, "r") as _token_file:
    token = _token_file.readline()

bot.run(token)
