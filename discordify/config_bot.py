"""A module used to configure discord bots"""
import logging
import builtins
import typing as T
import json
import importlib
import yaml
import discord
from discord.ext import commands
from discordify.commands import register_sync_func, on_message_closure

# example app config
# {
#     "name": "test_app",
#     "command_prefix": "$",
#     "commands": {"locals": {"function": "test_app.get_locals"}},
# }
logger = logging.getLogger(__name__)


def _get_fn_from_name(fn_name: str) -> T.Callable:

    python_path_list = fn_name.split(".")

    if len(python_path_list) == 1:
        fn_name = python_path_list[0]
        module = builtins
    else:
        fn_name = python_path_list[-1]
        module_path = ".".join(python_path_list[:-1])
        module = importlib.import_module(module_path)

    fn = getattr(module, fn_name)
    return fn


def _setup_bot(app_config: T.Dict[str, T.Any]) -> commands.Bot:
    """Iterate through app config and create app

    Args:
        app_config: dictionary that contains configs for the app
    """
    app_name = app_config["name"]
    command_prefix = app_config["command_prefix"]

    bot = commands.Bot(command_prefix=command_prefix)

    register_channel_command: T.Callable[[T.Callable, str], bool] = on_message_closure(
        bot
    )

    @bot.event
    async def on_ready():
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"to help at {command_prefix}help",
            )
        )

    if "commands" in app_config:
        for command_name, command_props in app_config["commands"].items():

            try:
                fn = _get_fn_from_name(command_props["function"])
            except:
                logger.exception("%s not found", command_props["function"])
                continue

            register_sync_func(bot, fn, command_name)

    if "channel-commands" in app_config:
        for command_name, command_props in app_config["channel-commands"].items():

            try:
                fn = _get_fn_from_name(command_props["function"])
            except:
                logger.exception("%s not found", command_props["function"])
                continue

            register_channel_command(fn, command_props["channel"])

    return bot


def parse_yaml(filename) -> commands.Bot:
    """Parse yaml config file"""
    with open(filename, "rb") as _file:
        app_config = yaml.load(_file, Loader=yaml.SafeLoader)

    return _setup_bot(app_config)


def parse_json(filename) -> commands.Bot:
    """Parse json config file"""
    with open(filename, "rb") as _file:
        app_config = json.load(_file)

    return _setup_bot(app_config)
