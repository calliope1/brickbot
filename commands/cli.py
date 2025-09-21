from exceptions import *

async def list_channels(client):
    """List all channels and guilds that the bot is part of."""
    # Probably doesn't need to be async
    for guild in client.guilds:
        responsetext = f"Guild -- **{guild}**: {guild.id}\n"
        for channel in guild.text_channels:
            responsetext += f"\n**{channel}**: {channel.id}"
        return responsetext

async def channel_info(client, channel_id):
    """Return the channel name, id and guild of a given channel (by its id)."""
    try:
        channel = client.get_channel(channel_id)
        return f"Channel is `{channel}`, id=`{channel.id}` in guild `{channel.guild}`."
    except:
        raise NoChannelException(channel_id)

async def extract_id(message, prefix):
    """Extract a channel id from the message after a prefix and a space.

    Message can also be a string.

    Returns
    -------
        int, str
    int: Channel id. 0 if there is a failure.
    str: Any additional text after the channel id

    Exceptions
    ----------
    TooShortMessageException: If there isn't enough room for an id after the prefix.
    NonIntIdException: If the id string cannot be parsed as an int.
    """
    if isinstance(message, str):
        message_content = message
    else:
        message_content = message.content
    if len(message_content) < len(prefix) + 19:
        raise TooShortMessageException(message_content, len(prefix) + 19)
    try:
        channel_id = int(message_content[len(prefix)+1 : len(prefix)+19])
    except:
        raise NonIntIdException(message_content[len(prefix)+1 : len(prefix)+19])
    # The + 20 accounts for a trailing space
    if len(message_content) > len(prefix) + 20:
        return channel_id, message_content[len(prefix)+20:]
    return channel_id, ""

async def delete_message(client, channel_id, message_id):
    """Delete the message in channel <channel_id> with id <message_id>."""
    try:
        target_channel = client.get_channel(channel_id)
    except:
        raise NoChannelException(channel_id)
    try:
        target_message = await target_channel.fetch_message(message_id)
    except:
        raise NoMessageException(message_id, channel_id)
    await target_message.delete()
    return target_channel, target_message