import typing as T
import json
import discord
import yaml
import importlib
from discord.ext import commands
from discordify.commands import register_sync_func

# example app config
# {
#     "name": "test_app",
#     "command_prefix": "$",
#     "commands": {"locals": {"function": "test_app.get_locals"}},
# }


def _register_functions(app_config: T.Dict[str, T.Any]) -> commands.Bot:
    """Iterate through app config and create app

    Args:
        app_config: dictionary that contains configs for the app
    """
    app_name = app_config["name"]
    command_prefix = app_config["command_prefix"]

    bot = commands.Bot(command_prefix=command_prefix)

    @bot.event
    async def on_ready():
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"to help at {command_prefix}help",
            )
        )

    for command_name, command_props in app_config["commands"].items():

        python_path_list = command_props["function"].split(".")
        fn_name = python_path_list[-1]
        module_path = ".".join(python_path_list[:-1])

        module = importlib.import_module(module_path)
        fn = getattr(module, fn_name)

        register_sync_func(bot, fn, command_name)

    return bot


def parse_yaml(filename) -> commands.Bot:
    """Parse yaml config file"""
    with open(filename, "rb") as _file:
        app_config = yaml.load(_file, Loader=yaml.SafeLoader)

    return _register_functions(app_config)


def parse_json(filename) -> commands.Bot:
    """Parse json config file"""
    with open(filename, "rb") as _file:
        app_config = json.load(_file)

    return _register_functions(app_config)
