from re import split
import discord
#intents = discord.Intents().all()
import asyncio
import time
import random

from discord import channel

from generation import Generate
from filedata import FileInteraction
from storing import Storage

client = discord.Client()

# test channel: 856539548488826880
# test server:712462824823062669
# test user: 231758930630410240

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await scrape_server(343794076849668096)
    while True:
        message, userID = await create_new_message(343794076849668096) #Server ID
        await post_as_webhook(userID, 343794076849668096, message) #server ID
        print("done")


async def scrape_server(serverID):
    channel_dict_list = FileInteraction.get_yaml_data("channels", serverID)
    channels = list(channel_dict_list[0].keys())
    full_message_dict = await asyncio.gather(*[scrape_channel(channelID) for channelID in channels])
    print("fully done")
    
    final_msg_dict = {}
    for message_dict in full_message_dict:
        for userID in message_dict:
            for value in message_dict[userID]:
                final_msg_dict.setdefault(userID, []).append(value)
    for userID in final_msg_dict:
        print(userID)
        #if await Storage.check_message_author(serverID, await client.fetch_user(userID)) and not userID in await Storage.get_bans(client, serverID):
        FileInteraction.add_list_to_user(userID, final_msg_dict[userID], serverID)

async def predicate(message):
    return not message.author.bot and not message.author.id in FileInteraction.get_yaml_data("users_to_ignore", message.guild.id)# and not message.author.id in await Storage.get_bans(client, message.guild.id)

async def scrape_channel(channelID):
    message_dict = dict()
    first_message = True
    curr_channel = client.get_channel(channelID)
    messages = await curr_channel.history(limit=10000).filter(predicate).flatten()
    for message in messages:
        if(first_message):
            FileInteraction.write_latest_message(message.guild.id, message.channel.id, message.id)
            first_message = False
        message_dict.setdefault(message.author.id, []).append([message.id, channelID])
    print("done scraping")
    return message_dict

async def post_as_webhook(userID, serverID, message):
    print("UserID:")
    print(userID)
    client.guild_subscriptions = True
    temp_channel_store = client.get_channel(FileInteraction.get_yaml_data("channel_to_post", serverID))
    webhook_list = await temp_channel_store.webhooks()
    myWebhook = None
    for webhook in webhook_list:
        if webhook.name == 'User Message Poster':
            myWebhook = webhook

    if not webhook_list:
        print("Webhook list empty!")
        try:
            myWebhook = await temp_channel_store.create_webhook(name='User Message Poster')
        except Exception as e:
            print(e)
    else:
        print("Already a webhook in here!")
    try:
        guild = client.get_guild(serverID)
        user_nickname = await guild.fetch_member(userID)
        user_avatar = await client.fetch_user(userID)
        await myWebhook.send(content=message, username=user_nickname.display_name, avatar_url=user_avatar.avatar_url)
    except:
        user_nickname = "Deleted User"
        user_avatar = None
        await myWebhook.send(content=message, username=user_nickname, avatar_url=user_avatar)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

async def create_new_message(serverID):
    user_file, userID = FileInteraction.read_random_file(serverID)
    unrolled_messages = await asyncio.gather(*[Generate.unroll_message(client, line) for line in user_file])
    FileInteraction.create_gen_file(serverID, unrolled_messages)
    pos_dict, markov_dict, pos_pattern = await Generate.tag_and_split(serverID)
    #pos_pattern = ["N", "V", "A"]
    next_word = ""
    created_message = ""
    print(pos_pattern)
    print("\n")
    print(pos_dict)
    print("\n")
    print(markov_dict)
    print("\n")
    for pos in pos_pattern:
        print("pos below")
        print(pos)
        print("\n")
        print("next word below")
        print(next_word)
        print("\n")
        try:
            intersection_list = intersection(pos_dict[pos], markov_dict[next_word])
        except Exception as e:
            print(e)
        if intersection_list:
            print(intersection_list)
            next_word = random.choice(intersection_list)
        else:
            print(random.choice(list(pos_dict[pos])))
            next_word = random.choice(list(pos_dict[pos]))
        print(next_word)
        print("\n")
        if next_word in ["@everyone", "@here", "everyone", "here"]:
            next_word = next_word[:-1] + " " + next_word[-1]
        created_message += next_word
        created_message += " "
    print(created_message)
    return created_message[:-1], userID

@client.event
async def on_message(message):
    """Checks if the server directory for the message has been created.
    Check if the message author is valid.
    Adds the message to the user's file.
    Sorts all files in the server directory.
    
    message: Message object containing information about the newly-sent discord message."""
    if(FileInteraction.check_existence(message.guild.id)):
        if(await Storage.check_message_author(message.guild.id, message.author)):
            FileInteraction.add_message_to_user(message.author.id, message.id, message.channel.id, message.guild.id)
            FileInteraction.write_latest_message(message.guild.id, message.channel.id, message.id)
            #FileInteraction.sort_all_files(message.guild.id) # Maybe a seperate function to just sort one file? Would be better...

def get_token():
    f = open("token.txt", "r")
    token = f.readline().strip()
    return token

client.run(get_token())