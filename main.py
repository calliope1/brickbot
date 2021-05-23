import discord
import os
import random
import re
import brickbot_arg

from dotenv import load_dotenv

# Brickbot invite link
# https://discord.com/api/oauth2/authorize?client_id=819688841527033927&permissions=265280&scope=bot

# dotenv variable grabbing
load_dotenv()
token = str(os.getenv("discord_token"))
excluded_channel = int(os.getenv("excluded_channel"))
commands_channel = int(os.getenv("commands_channel"))
promoted_channel = int(os.getenv("promoted_channel"))


#Discord client connection
client = discord.Client(activity=discord.Game(name="Brick"))

#Brick counting
client.brickcount = 0

#Emojis
client.brick = "<:brick:834492870353485844>"
client.picklebrick = "<:PickleBrick:834492890272628836>"
client.brick_lesbian = "<:brick_lesbian:836037661340205076>"
#client.OwO = "<:OwO:834511912121270303>"
client.brick_beer = "<:brick_beer:842065415840858122>"
client.thank_you = "<:thank_you:846033897296756756>"
client.extreme_sadness = "<:extreme_sadness:846033897392439306>"

#Regular expression looking for bricks
client.regex = re.compile('[b8]+r+[i1!]*c+[ck]')

#Custom character strip for regex testing
def isregular(character):
    if character.isalpha():
        return True
    elif character in ['8','1','!']:
        return True
    else:
        return False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    #Don't react to your own messages
    if message.author == client.user:
        return
    
    #Don't interact with excluded channels
    if message.channel.id == excluded_channel:
        return
    
    #The commands channel in brickbot's server
    elif message.channel.id == commands_channel:
    
        #Return list of channels that brickbot is in
        if message.content.lower() == "!channels":
            for guild in client.guilds:
                responsetext = "Guild -- **" + str(guild) + "**: " + str(guild.id) + "\n"
                for channel in guild.text_channels:
                    responsetext += "\n**" + str(channel) + "**: " + str(channel.id)
                await message.channel.send(responsetext)
                
        #Returns the name and guild of a particular channel id
        elif message.content.lower()[0:12] == "!channelname":
            channel = client.get_channel(int(message.content[13:31]))
            await message.channel.send("Channel is `" + str(channel) + "`, id=`" + str(channel.id) + "` in guild `" + str(channel.guild) + "`.")
            
        #Sends a message to the channel id (syntax: !sendmessage CHANNELID message)
        elif message.content.lower()[0:12] == "!sendmessage":
            channel = client.get_channel(int(message.content[13:31]))
            await channel.send(message.content[32:len(message.content)])
            await message.channel.send("Sent message '" + message.content[32:len(message.content)] + "' to channel '" + str(channel) + "'")
        
        #Deletes a message based on its id (syntax: !deletemessage MESSAGEID CHANNELID)
        elif message.content.lower()[0:14] == "!deletemessage":
            channel = client.get_channel(int(message.content[34:52]))
            msg = await channel.fetch_message(int(message.content[15:33]))
            await msg.delete()
            await message.channel.send("Deleted message '" + msg.content + "' from channel '" + str(channel) + "'")
        
        #Echoes a message in print
        elif message.content.lower()[0:5] == "!echo":
            await message.channel.send("Echoing message!")
            print(message.content[6:len(message.content)])
        
        #Brick reacts a maessage (syntax: !brickreact MESSAGEID CHANNELID)
        elif message.content.lower()[0:11] == "!brickreact":
            channel = client.get_channel(int(message.content[31:49]))
            msg = await channel.fetch_message(int(message.content[12:30]))
            await msg.add_reaction(client.brick)
            await message.channel.send("Reacted to message '" + msg.content + "' with " + client.brick)
        
        #Brick_beer reacts a maessage (syntax: !brickbeerreact MESSAGEID CHANNELID)
        elif message.content.lower()[0:15] == "!brickbeerreact":
            channel = client.get_channel(int(message.content[35:54]))
            msg = await channel.fetch_message(int(message.content[16:34]))
            await msg.add_reaction(client.brick_beer)
            await message.channel.send("Reacted to message '" + msg.content + "' with " + client.brick_beer)
        
            
        
        #No known command
        else:
            await message.channel.send("Command failed")
    
    #!bb-help command
    elif message.content.lower() == "!bb-help":
        await message.channel.send("Current brickbot commands are:\n•`!bb-help`\tThat's this command!\n•`!areyoutherebb`\tI'll respond with 'Yes' (if I'm online)\n•`!brickcount`\tCounts the number of bricks located since the last count (sorta)\n•`!brickbot`\tApproximate explanation of who I am\n•`!brickrepo`\tI'll link my GitHub repository!")
        print("!bb-help command in channel " + str(message.channel))
    
    #Is brickbot online command
    elif message.content.lower() == "!areyoutherebb":
        await message.channel.send("Yes! " + client.brick)
        
    #Brickcount command
    elif message.content.lower() == "!brickcount":
        if client.brickcount == 0:
            await message.channel.send("There have been no bricks since the last count! " + client.brick)
        elif client.brickcount == 1:
            await message.channel.send("There has been 1 brick since the last count! " + client.brick)
        else:
            await message.channel.send("There have been " + str(client.brickcount) + " bricks since the last count! " + client.brick)
        print("Brickcount for " + str(client.brickcount) + " bricks in channel " + str(message.channel))
        client.brickcount = 0
        
    #Who is brickbot command
    elif message.content.lower() == "!brickbot":
        await message.channel.send("Brickbot is a bot that reacts to any messages containing the word brick with a " + client.brick + "! For a full list of commands, type '!bb-help'.")
        print("!brickbot in channel " + str(message.channel))
    
    #Brickbot repository command
    elif message.content.lower() == "!brickrepo":
        await message.channel.send("You can find the repository of my code at https://github.com/calliope1/brickbot")
        print("Brickrepo command activated in channel " + str(message.channel))
    
    #Lesbian reaction
    elif "lesbian" in message.content.lower():
        await message.add_reaction(client.brick_lesbian)
        print("Lesbian reacted in " + str(message.channel))
    
    #Secret pickle brick command
    elif message.content.lower() == "pickle brick":
        await message.add_reaction(client.picklebrick)
        await message.channel.send("I'm Pickle Brick!! " + client.picklebrick)
        print("Pickle brick in channel " + str(message.channel))
    
    #Brickbot yes command
    elif "brickbot yes" in message.content.lower():
        await message.add_reaction(client.thank_you)
        await message.channel.send(client.thank_you)
        print("Brickbot yes in channel " + str(message.channel))
    
    #Brickbot no command
    elif "brickbot no" in message.content.lower():
        await message.add_reaction(client.extreme_sadness)
        await message.channel.send(client.extreme_sadness)
        print("Brickbot no in channel " + str(message.channel))
    
    #Regex syntax matching
    elif bool(client.regex.search("".join(filter(isregular,message.content.lower())))) or bool(client.regex.search("".join(filter(isregular,message.content.lower()[::-1])))):
        await message.channel.send(client.brick)
        await message.add_reaction(client.brick)
        client.brickcount += 1
        print("Brick located in channel " + str(message.channel))
    
    #Did someone say brick??
    elif "brick" in "".join(filter(str.isalpha,message.content.lower())) or "🧱" in message.content.lower() or client.brick in message.content.lower():
        await message.channel.send(client.brick)
        await message.add_reaction(client.brick)
        client.brickcount += 1
        print("Brick located in channel " + str(message.channel))
        
    #React to pub messages from promoted channels with :brick_beer:
    elif message.channel.id == promoted_channel:
        if "pub" in message.content.lower():
            await message.channel.send(client.brick_beer)
            await message.add_reaction(client.brick_beer)
            print("Pub reacted to an announcement")
        elif not random.randint(0,19):
            await message.add_reaction(client.brick)
            print("Brick reacted to an announcement")
    
    #React to every hundredth (randomly) message with :brick:
    elif not random.randint(0,99):
        await message.add_reaction(client.brick)
        print("Brick reacted in channel " + str(message.channel))

#Logs in to the bot
client.run(token)