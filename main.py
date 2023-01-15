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



client.run(os.getenv('TOKEN'))