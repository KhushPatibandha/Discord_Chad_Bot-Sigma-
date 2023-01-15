import discord
import os
import random
import requests
import json
import asyncio
import youtube_dl
from dotenv import load_dotenv
load_dotenv()

client = discord.Client(intents=discord.Intents.all())

block_words = ["peepee", "poopoo", "angry", "https://", "http://"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] +" -"+ json_data[0]['a']
    return quote

voice_clients = {}

yt_dl_opts = {'format' : 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options' : '-vn'}

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(msg):
    print(msg.author)
    print(msg.content)
    if(msg.author == client.user):
        return

    if(msg.content.lower().startswith("$hi")):
        await msg.channel.send(f"Hi, {msg.author.display_name}")

    for text in block_words:
        if("Mod" not in str(msg.author.roles) and text in str(msg.content.lower())):
            # await msg.author.ban()
            await msg.delete()
            return
    print("Not Deleting...")

    if(msg.content.startswith('$inspire')):
        await msg.channel.send(get_quote())

    if(msg.content.startswith("$play")):

        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("Error")

        try:
            url = msg.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

            voice_clients[msg.guild.id].play(player)

        except Exception as err:
            print(err)

    if(msg.content.startswith("$pause")):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    if(msg.content.startswith("$resume")):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)  

    if(msg.content.startswith("$stop")):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)


client.run(os.getenv('TOKEN'))