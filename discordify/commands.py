"""A module to register bot commands"""
import inspect
import logging
import typing as T
from discord import channel
import discord
from discord.ext import commands
from discordify.messages import create_msg, parse_reply, np_array_from_png_bytes, _is_image

logger = logging.getLogger(__name__)

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

def on_message_closure(bot: commands.Bot):

    channel_specific_commands = {}

    def register_channel_command(fn: T.Callable, channel_name: str) -> bool:
        if channel_name in channel_specific_commands:
            logger.warning("channel %s already has a function registered to it", channel_name)
            return False
        
        if len(inspect.signature(fn).parameters) != 1:
            return False

        channel_specific_commands[channel_name] = fn
        return True
    
    @bot.event
    async def on_message(msg: discord.Message):
        if msg.author == bot.user:
            return
            
        channel_name = msg.channel.name
        if channel_name in channel_specific_commands:
            logger.info("Found command matching channel...")
            logger.info("Do some processing to check if inputs are acceptable")

            # TODO: figure out preprocessing
            assert (msg.content == '' or msg.attachments == [])
            try:
                if msg.content != '':
                    channel_specific_commands[channel_name](msg.content)
                else:
                    png_ = await msg.attachments[0].read()
                    np_arr = np_array_from_png_bytes(png_)
                    result = channel_specific_commands[channel_name](np_arr)
                    reply = parse_reply(result)
                    logger.debug(reply)
                    logger.debug("Is image %s", _is_image(result))
                    reply = create_msg(**reply)
                    await msg.channel.send(**reply)
            except:
                logger.exception("Error occured while calling function")
    return register_channel_command
        
