"""A module to register bot commands"""
import typing as T
from discord.ext import commands


def register_sync_func(
    bot: commands.Bot, fn: T.Callable, name: str = None, replace: bool = False
):
    """Registers a Callable object as a bot command

    This callable object can then be invoked using
    {command_prefix}{name} {arg1} {arg2} ...

    Args:
        fn: The function to be registered
        name: Optional. If provided the command will be registered with the
            given name. If this arg is not provided, the name will default to
            the name of the original function.
        replace: Optional. This flag indicates whether this command can replace
            existing commands with the same name.
    """
    if name is None:
        name = fn.__name__

    @bot.command(name)
    async def wrapper(ctx: commands.Context, *args, **kwargs):
        await ctx.send(fn(*args, **kwargs))
        # TODO: insert reply mechanisms

    return wrapper
