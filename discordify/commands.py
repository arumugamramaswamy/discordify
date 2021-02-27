"""A module to register bot commands"""
import inspect
import typing as T
from discord.ext import commands
from discordify.messages import create_msg, parse_reply

def _copy_signature(source_fct): 
    def copy(target_fct):
        params = inspect.signature(target_fct).parameters
        ctx_type = (list(params.values())[0])
        try:
            calling_type = list(inspect.signature(source_fct).parameters.values())
            target_fct.__signature__ = inspect.Signature([ctx_type]+calling_type)
        except:
            pass
        return target_fct 
    return copy 

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

    help_str = inspect.getdoc(fn)

    @bot.command(name=name, help=help_str)
    @_copy_signature(fn)
    async def wrapper(ctx: commands.Context, *args, **kwargs):
        reply = fn(*args, **kwargs)

        parsed_reply = parse_reply(reply)
        msg = create_msg(**parsed_reply)
        await ctx.send(**msg)

    return wrapper
