import os
from sys import argv

know_config_types = {"json", "yaml"}

# check for config type
if len(argv) == 1:
    print("Config type not provided defaulting to json")
    config_type = "json"
else:
    config_type = argv[1]
    if config_type not in know_config_types:
        print("Unknown config type detected, defaulting to json")
        config_type = "json"

# create config directory
try:
    os.mkdir("discordify-config")
except:
    print("Config folder already exists... skipping")

# Create and ignore token
if os.path.exists(os.path.join("discordify-config", "token.dcfy")):
    print("Token already exists... skipping")
else:
    with open((os.path.join("discordify-config", ".gitignore")), "w") as _file:
        _file.writelines(["token.dcfy"])

    with open((os.path.join("discordify-config", "token.dcfy")), "w") as _file:
        _file.writelines(["token goes here"])

# Create config file
config_file_name = f"config.{config_type}"

if os.path.exists(os.path.join("discordify-config", config_file_name)):
    print("Config.json already exists... skipping")
else:
    with open((os.path.join("discordify-config", config_file_name)), "w") as _file:
        # TODO: provide example configs to start with
        _file.writelines([""])
