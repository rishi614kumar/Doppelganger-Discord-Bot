# doppelganger_bot.py
import os
import sys
import random
import discord
import pandas as pd
import random
import asyncio

import gpt_2_simple as gpt2
from datetime import datetime

from discord.utils import get
from discord import FFmpegPCMAudio

from discord.ext import commands

#~~~enter your information here~~~ 
#the token of your discord bot
YOUR_BOT_TOKEN = ''
#the name of your main discord server
YOUR_GUILD = ''
#the name of your saved model
YOUR_MODEL_NAME = 'doppelganger'
#the integer ids of channels you wish to pull messages from
YOUR_CHANNEL_LIST = []
#the full discord usernames of the people you want to pull messages for. Just 'everyone' for everyone
YOUR_CHOSEN_USERS = ['everyone']
#your JSON file with the clean and parsed chats. For fast loading purposes
YOUR_FULL_JSON = 'master.json'
#the name for your generated text file
YOUR_GENERATED_FILE = 'doppel_gen.txt'
#your preferred command prefix
YOUR_PREFIX = '!'
#your preferred keyword
YOUR_KEYWORD = 'doppelganger'

master_df = pd.read_json(YOUR_FULL_JSON)
sess = gpt2.start_tf_sess()
load=0
doppel_gen = []


TOKEN = YOUR_BOT_TOKEN
GUILD = YOUR_GUILD
model_name = YOUR_MODEL_NAME


client = commands.Bot(command_prefix=YOUR_PREFIX)


@client.event
#on successful connection the activity and status of the bot are set
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    activity = discord.Activity(name="English - for Dummies", type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)

#a simple test command
@client.command(name='doppelganger')
async def doppelganger(ctx):
    response = "It is I, the doppelganger."
    await ctx.send(response)

#list the ids of all currently connected channels
@client.command(name="list")
async def channels(ctx):
    for channel in client.get_all_channels():
        print(id)

#scrape the messages from your desired channels into a json file for each channel as a seperate file
@client.command(name="scrape")
async def history(ctx):  
    print("scan request received...")
    df=pd.DataFrame({'User': [], 'Message_ID': [], 'Channel': [], 'Date': [], 'Message': []})
    channel_list = YOUR_CHANNEL_LIST
    count=1
    for id in channel_list:
        print("on "+str(count)+" of "+str(len(channel_list)))
        count=count+1
        print("getting messages...")
        messages = await client.get_channel(id).history(limit=9999999).flatten()
        print("building...")
        for message in messages:
            new_row = {'User': str(message.author.name)+'#'+str(message.author.discriminator), 'Message_ID': message.id , 'Channel': str(message.channel.name), 'Date': message.created_at, 'Message': str(message.clean_content)}
            df = df.append(new_row, ignore_index = True)
        df.to_json(r'channel_messages'+str(count)+'.json')
        print("wrote to file successfully")

#scrape the messages from your desired channels into a single json file
@client.command(name='longscrape')
async def long_history(ctx):
    print("long scan request received")
    df=pd.DataFrame({'User': [], 'Message_ID': [], 'Channel': [], 'Date': [], 'Message': []})
    channel_list = YOUR_CHANNEL_LIST
    print("getting messages...")
    count=1
    for id in channel_list:
        async for message in client.get_channel(id).history(limit=999999999):
            new_row = {'User': str(message.author.name)+'#'+str(message.author.discriminator), 'Message_ID': message.id , 'Channel': str(message.channel.name), 'Date': message.created_at, 'Message': str(message.clean_content)}
            df = df.append(new_row, ignore_index = True)
            if count%5000==0:
                df.to_json(r'long_channel_messages.json')
                print("wrote to file successfully") 
            count=count+1
        print("finished!")

#sends a random message that one of your chosen users have sent before. a fun guessing game
@client.command(name='roulette')
async def roulette(ctx):
    users = YOUR_CHOSEN_USERS
    phrase=''
    rand = random.randint(0, len(users) - 1)
    users_dict = {}
    for i in range(len(users)):
        users_dict[i]=users[i] 
    chosen = users_dict[rand]
    users_series=master_df[master_df['Name']==chosen]['Message'].reset_index()['Message']
    spaces=""
    for i in range(0,7-len(chosen)):
        spaces=spaces+" "
    name_add=chosen+spaces
    spoilers=''
    spoilers=" ||"+name_add+"\t||"
    while phrase=='':
        rand_index = random.randint(0,len(users_series))
        phrase= users_series[rand_index]
    response = phrase+spoilers
    if phrase!='':
        await ctx.send(response)


@client.event
#sends a random message that one of your chosen users have sent before when the keyword is typed
async def on_message(message):
    keyword=YOUR_KEYWORD
    users = YOUR_CHOSEN_USERS
    if client.user.id != message.author.id:
        if keyword.lower() in message.content.lower():
            phrase=''
            rand = random.randint(0,len(users) - 1)
            users_dict = {}
            for i in range(len(users)):
                users_dict[i]=users[i]
            chosen = users_dict[rand]
            users_series=master_df[master_df['Name']==chosen]['Message'].reset_index()['Message']
            
            while phrase=='':
                rand_index = random.randint(0,len(users_series))
                phrase=boy_series[rand_index]
            response = phrase
            if phrase!='':
                await message.channel.send(response)

    await client.process_commands(message)

#run this command on startup to load the model and generate starting text
@client.command(name='load')
async def start_up(ctx):
    global load
    global model_name
    global doppel_gen
    
    if load==1:
        print("ALREADY LOADED!")
        return
    print('initializing...')
    gpt2.load_gpt2(sess, run_name=model_name)
    print("intialized!")
    
    
    gen_file = YOUR_GENERATED_FILE
    print("loading generated text...")
    context=''
    try:
        response = gpt2.generate_to_file(sess,destination_path=gen_file, run_name=model_name, temperature=0.9, nsamples=20, batch_size=20, length=350)
        print("done generating!!")
    except:
        print("error! continuing with partial data...")
    file = open(str(gen_file))
    doppel_gen = file.read().split("====================")
    file.close()
    print(str(gen_file)+" loaded!")
    load=1

#command to manually refresh the generated text
@client.command(name='refresh')
async def reload(ctx):
    global load
    global doppel_gen
    global model_name

    if load==0:
        print("NOT LOADED!")
        return
    gen_file = YOUR_GENERATED_FILE
    print("reloading generated text...")
    try:
        response = gpt2.generate_to_file(sess,destination_path=gen_file, run_name=model_name, temperature=0.9, nsamples=20, batch_size=20, length=350)
        print("done generating!!")
    except:
        print("error! continuing with partial data...")
    file = open(str(gen_file))
    doppel_gen = file.read().split("====================")
    file.close()
    print(str(gen_file)+" refreshed!")


 
def reload_doppelganger():
    global load
    global doppel_gen
    global model_name

    
    if load==0:
        print("NOT LOADED!")
        return
    gen_file = YOUR_GENERATED_FILE
    print("reloading generated text...")
    try:
        response = gpt2.generate_to_file(sess,destination_path=gen_file, run_name=model_name, temperature=0.9, nsamples=20, batch_size=20, length=350)
        print("done generating!!")
    except:
        print("error! continuing with partial data...")
    file = open(str(gen_file))
    doppel_gen = file.read().split("====================")
    file.close()
    print(str(gen_file)+" refreshed!")


#sends generated text and acts as if a human typed it
@client.command("generate")
async def generate(ctx):
    global load
    global doppel_gen

    if load==0:
        print("NOT LOADED!")
        return
    if len(doppel_gen)==0:
        print("batch list is empty!")
        reload_doppelganger()
    
    chosen_batch_position = random.randint(0,len(doppel_gen)-1)

    batch=doppel_gen[chosen_batch_position].split('\n')

    doppel_gen.pop(chosen_batch_position)
    MAX_LENGTH = 4

    length_of_message = random.randint(1,MAX_LENGTH)

    position_in_batch = random.randint(0,max(4,len(batch)-1-length_of_message))

    good_msg=[]
    async with ctx.typing():
        for msg in batch[position_in_batch:position_in_batch+length_of_message]:
            #if the doppelganger sends nothing, then length of message was 1 and the content was ''
            if msg!='':
                good_msg.append(msg)
        if len(good_msg)>0:
            for gmsg in good_msg:
                await asyncio.sleep(random.uniform(0.5, 2))
                await ctx.send(gmsg)
    
    

#start the bot
client.run(TOKEN)
print("code stopped.")