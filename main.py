import discord
import os
import random
import re
import commands.cli as cli
from commands.exceptions import *

from dotenv import load_dotenv

# Brickbot invite link
# https://discord.com/api/oauth2/authorize?client_id=819688841527033927&permissions=265280&scope=bot

# dotenv variable grabbing
load_dotenv()
token = os.getenv("discord_token")
excluded_channels = [int(os.getenv("excluded_channel_1")),int(os.getenv("excluded_channel_2"))]
commands_channel = int(os.getenv("commands_channel"))
promoted_channel = int(os.getenv("promoted_channel"))

#Discord client connection
client = discord.Client(activity=discord.Game(name="Brick"))

#Brick counting
client.brickcount = 0

#Emojis
#Brick-type (non-flag)
client.brick = str(os.getenv("brick"))
client.pickle_brick = str(os.getenv("pickle_brick"))
client.brick_beer = str(os.getenv("brick_beer"))
client.brick_sign = str(os.getenv("brick_sign"))
client.party_brick = str(os.getenv("party_brick"))
#Flags
client.brick_lesbian = str(os.getenv("brick_lesbian"))
client.brick_ace = str(os.getenv("brick_ace"))
client.brick_bi = str(os.getenv("brick_bi"))
client.brick_lgbt = str(os.getenv("brick_lgbt"))
client.brick_nb = str(os.getenv("brick_nb"))
client.brick_trans = str(os.getenv("brick_trans"))
#Others
client.thank_you = str(os.getenv("thank_you"))
client.extreme_sadness = str(os.getenv("extreme_sadness"))

#Flag list (for random calling)
client.all_flags = [client.brick_ace,client.brick_bi,client.brick_lesbian,client.brick_lgbt,client.brick_nb,client.brick_trans]

#Regular expression looking for bricks
client.regex = re.compile('[b8]+r+[i1!]*c+[ck]')

#Custom character strip for regex testing
def isregular(character):
    return character.isaplha() or character in {'8', '1', '!'}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    #Don't react to your own messages
    if message.author == client.user:
        return 0
    
    #In fact, don't react to any bots' messages
    if message.author.bot:
        return 0
    
    #Don't interact with excluded channels
    if message.channel.id in excluded_channels:
        return 0
    
    #The commands channel in brickbot's server
    if message.channel.id == commands_channel:
    
        #Return list of channels that brickbot is in
        if message.content.lower() == "!channels":
            await message.channel.send(cli.list_channels(client))
            return 0
                
        #Returns the name and guild of a particular channel id
        elif message.content.lower()[0:12] == "!channelname":
            try:
                channel_id, extra = cli.extract_id(message, "!channelname")
            except NonIntIdException as niie:
                await message.channel.send(f"Error: {niie.message}")
                return NonIntIdException.value
            except TooShortMessageException as tsme:
                await message.channel.send(f"Error: {tsme.message}")
                return TooShortMessageException.value
            if extra:
                await message.channel.send(f"Warning: Channel id exceeded 18 characters. Cutting down to {channel_id}")
            try:
                await message.channel.send(cli.channel_info(client, channel_id))
                return 0
            except NoChannelException as nce:
                await message.channel.send(nce.message)
                return NoChannelException.value
            return UnexpectedLogicPath.value
            
        #Sends a message to the channel id (syntax: !sendmessage CHANNELID message)
        elif message.content.lower()[0:12] == "!sendmessage":
            try:
                channel_id, extra = cli.extract_id(message, "!sendmessage")
            except NonIntIdException as niie:
                await message.channel.send(f"Error: {niie.message}")
                return NonIntIdException.value
            except TooShortMessageException as tsme:
                await message.channel.send(f"Error: {tsme.message}")
                return TooShortMessageException.value
            try:
                channel = client.get_channel(channel_id)
            except:
                exception = NoChannelException(channel_id)
                message.channel.send(f"Error: {exception.message}")
                return NoChannelException.value
            if not extra:
                await message.channel.send("No message to send.")
                return 0
            await channel.send(extra)
            return 0
        
        #Deletes a message based on its id (syntax: !deletemessage MESSAGEID CHANNELID)
        elif message.content.lower()[0:14] == "!deletemessage":
            message_id, raw_channel_id = cli.extract_id(message, "!deletemessage")
            if not message_id:
                await message.channel.send(f"Error: Malformed message id. Either the id is too short or it is not an int.")
                return
            channel_id, extra = cli.extract_id(raw_channel_id, "")
            if not channel_id:
                await message.channel.send(f"Error: Malformed channel id. Either the id is too short or it is not an int.")
                return
            if extra:
                await message.channel.send(f"Warning: Additional message content `{extra}` will be discarded.")
            try:
                target_channel, target_message = cli.delete_message(client, channel_id, message_id)
                await message.target_channel.send(f"Deleted message '{target_message.content}' from channel '{target_channel}'")
            except NoChannelException as nce:
                await message.channel.send(f"Error: {nce.message}")
            except NoMessageException as nme:
                await message.channel.send(f"Error: {nme.message}")
            finally:
                return

        #Echoes a message in print
        elif message.content.lower()[0:5] == "!echo":
            if len(message.content) < 6:
                await message.channel.send("No message to echo.")
                return 0
            await message.channel.send("Echoing message!")
            print(message.content[6:len(message.content)])
            return 0
        
        #Brick reacts a maessage (syntax: !brickreact MESSAGEID CHANNELID)
        elif message.content.lower()[0:11] == "!brickreact":
            try:
                message_id, raw_channel_id = cli.extract_id(message, "!brickreact")
            except NonIntIdException as niie:
                await message.channel.send(f"Error: {niie.message}")
                return NonIntIdException.value
            except TooShortMessageException as tsme:
                await message.channel.send(f"Error: {tsme.message}")
                return TooShortMessageException.value
            try:
                channel_id, extra = cli.extract_id(raw_channel_id, "")
            except NonIntIdException as niie:
                await message.channel.send(f"Error: {niie.message}")
                return NonIntIdException.value
            except TooShortMessageException as tsme:
                await message.channel.send(f"Error: {tsme.message}")
                return TooShortMessageException.value
            try:
                channel = client.get_channel(channel_id)
            except:
                exception = NoChannelException(channel_id)
                await message.channel.send(f"Error: {exception.message}")
                return NoChannelException.value
            try:
                target_message = await channel.fetch_message(message_id)
            except:
                exception = NoMessageException(message_id, channel_id)
                await message.channel.send(f"Error: {exception.message}")
                return NoMessageException.value
            await target_message.add_reaction(client.brick)
            await message.channel.send(f"Reacted to message '{target_message.content}' with {client.brick}.")
            return 0
        
        #Brick_beer reacts a maessage (syntax: !brickbeerreact MESSAGEID CHANNELID)
        elif message.content.lower()[0:15] == "!brickbeerreact":
            try:
                message_id, raw_channel_id = cli.extract_id(message, "!brickbeerreact")
            except NonIntIdException as niie:
                await message.channel.send(f"Error: {niie.message}")
                return NonIntIdException.value
            except TooShortMessageException as tsme:
                await message.channel.send(f"Error: {tsme.message}")
                return TooShortMessageException.value
            try:
                channel_id, extra = cli.extract_id(raw_channel_id, "")
            except NonIntIdException as niie:
                await message.channel.send(f"Error: {niie.message}")
                return NonIntIdException.value
            except TooShortMessageException as tsme:
                await message.channel.send(f"Error: {tsme.message}")
                return TooShortMessageException.value
            try:
                channel = client.get_channel(channel_id)
            except:
                exception = NoChannelException(channel_id)
                await message.channel.send(f"Error: {exception.message}")
                return NoChannelException.value
            try:
                target_message = client.get_message(message_id)
            except:
                exception = NoMessageException(message_id, channel_id)
                await message.channel.send(f"Error: {exception.message}")
                return NoMessageException.value
            await target_message.add_reaction(client.brick_beer)
            await message.channel.send(f"Reacted to message '{target_message.content}' with {client.brick_beer}")
            return 0
        
        #Experimental DM feature
        elif message.content.lower() == "!dmme":
            await message.author.send("Hi!")
            return 0

        #No known command
        await message.channel.send("Not a known command.")
        return 0
    
    # If bigotry is being mentioned, we don't want BrickBot barging in
    if "phobia" in message.content.lower():
        return 0

    #Flag reactions
    if "asexual" in message.content.lower() or " ace " in message.content.lower():
        await message.add_reaction(client.brick_ace)
        print(f"Asexual reacted in {message.channel}")
        return 0
    if "bisexual" in message.content.lower():
        await message.add_reaction(client.brick_bi)
        print(f"Bisexual reacted in {message.channel}")
        return 0
    if "lesbian" in message.content.lower():
        await message.add_reaction(client.brick_lesbian)
        print(f"Lesbian reacted in {message.channel}")
        return 0
    if "gay" in message.content.lower() or "lgbt" in message.content.lower() or "queer" in message.content.lower():
        await message.add_reaction(client.brick_lgbt)
        print(f"LGBT reacted in {message.channel}")
        return 0
    if "non-binary" in message.content.lower() or "nonbinary" in message.content.lower() or "non binary" in message.content.lower():
        await message.add_reaction(client.brick_nb)
        print(f"Non-binary reacted in {message.channel}")
        return 0
    if "trans" in message.content.lower():
        await message.add_reaction(client.brick_trans)
        print("Trans reacted in " + str(message.channel))
        return 0

    #!bb-help command
    if message.content.lower() == "!bb-help":
        await message.author.send("Current brickbot commands are:\n•`!bb-help`\tThat's this command! The command list is sent as a DM.\n•`!bb-help-here`\tI'll send this list to the channel, rather than as a DM\n•`!areyoutherebb`\tI'll respond with 'Yes' (if I'm online)\n•`!brickbot`\tApproximate explanation of who I am\n•`!brickrepo`\tI'll link my GitHub repository!")
        await message.channel.send("Command list sent as a direct message!")
        print(f"!bb-help command in channel {message.channel}")
        return 0
    
    #!bb-help-here command
    elif message.content.lower() == "!bb-help-here":
        await message.channel.send("Current brickbot commands are:\n•`!bb-help`\tSends my command list as a DM.\n•`!bb-help-here`\tThat's this command! I send my command list to the channel\n•`!areyoutherebb`\tI'll respond with 'Yes' (if I'm online)\n•`!brickbot`\tApproximate explanation of who I am\n•`!brickrepo`\tI'll link my GitHub repository!")
        print("!bb-help-here command in channel {message.channel}")
        return 0
    
    #Is brickbot online command
    elif message.content.lower() == "!areyoutherebb":
        await message.channel.send(f"Yes! {client.brick}")
        return 0
        
    # #Brickcount command
    # elif message.content.lower() == "!brickcount":
        # if client.brickcount == 0:
            # await message.channel.send("There have been no bricks since the last count! " + client.brick)
        # elif client.brickcount == 1:
            # await message.channel.send("There has been 1 brick since the last count! " + client.brick)
        # else:
            # await message.channel.send("There have been " + str(client.brickcount) + " bricks since the last count! " + client.brick)
        # print("Brickcount for " + str(client.brickcount) + " bricks in channel " + str(message.channel))
        # client.brickcount = 0
        
    #Who is brickbot command
    elif message.content.lower() == "!brickbot":
        await message.channel.send(f"Brickbot is a bot that reacts to any messages containing the word brick with a {client.brick}! For a full list of commands, type '!bb-help'.")
        print(f"!brickbot in channel {message.channel}")
        return 0
    
    #Brickbot repository command
    elif message.content.lower() == "!brickrepo":
        await message.channel.send("You can find the repository of my code at https://github.com/calliope1/brickbot")
        print(f"Brickrepo command activated in channel {message.channel}")
        return 0
    
    #Pickle brick
    elif "pickle brick" in message.content.lower():
        await message.add_reaction(client.pickle_brick)
        await message.channel.send(f"I'm Pickle Brick!! {client.pickle_brick}")
        print("Pickle brick in channel {message.channel}")
        return 0
        
    #Brickbot yes command
    elif "brickbot yes" in message.content.lower():
        await message.add_reaction(client.thank_you)
        await message.channel.send(client.thank_you)
        print(f"Brickbot yes in channel {message.channel}")
        return 0
    
    #Brickbot no command
    elif "brickbot no" in message.content.lower():
        await message.add_reaction(client.extreme_sadness)
        await message.channel.send(client.extreme_sadness)
        print(f"Brickbot no in channel {message.channel}")
        return 0
    
    #No fun command
    elif "no fun" in message.content.lower() or "nofun" in message.content.lower():
        await message.add_reaction(client.brick_sign)
        print(f"No fun reacted in channel {message.channel}")
        return 0
    
        #React to pub messages from promoted channels with :brick_beer:
    elif message.channel.id == promoted_channel:
        if "pub" in message.content.lower():
            await message.channel.send(client.brick_beer)
            await message.add_reaction(client.brick_beer)
            print("Pub reacted to an announcement")
            return 0
        elif bool(client.regex.search("".join(filter(isregular,message.content.lower())))) or bool(client.regex.search("".join(filter(isregular,message.content.lower()[::-1])))) or "🧱" in message.content.lower():
            if not random.randint(0,99):
                emoji = client.all_flags[random.randint(0,len(client.all_flags))]
                await message.channel.send(emoji)
                await message.add_reaction(emoji)
            else:
                await message.channel.send(client.brick)
                await message.add_reaction(client.brick)
            print(f"Brick found in channel {message.channel}")
            return 0
        elif not random.randint(0,19):
            await message.add_reaction(client.brick)
            print("Brick reacted to an announcement")
            return 0

    #Regex syntax matching and brick finding
    elif bool(client.regex.search("".join(filter(isregular,message.content.lower())))) or bool(client.regex.search("".join(filter(isregular,message.content.lower()[::-1])))) or "🧱" in message.content.lower():
        if not random.randint(0,99):
            emoji = client.all_flags[random.randint(0,len(client.all_flags))]
            await message.channel.send(emoji)
            await message.add_reaction(emoji)
        else:
            await message.channel.send(client.brick)
            await message.add_reaction(client.brick)
        print(f"Brick found in channel {message.channel}")
        return 0
    
    #React to every hundredth (randomly) message with :brick:
    elif not random.randint(0,99):
        if not random.randint(0,49):
            await message.add_reaction(client.party_brick)
        elif not random.randint(0,99):
            emoji = client.all_flags[random.randint(0,len(client.all_flags))]
            await message.add_reaction(emoji)
        else:
            await message.add_reaction(client.brick)
        print("Brick reacted in channel {message.channel}")
        return 0

#Logs in to the bot
client.run(token)