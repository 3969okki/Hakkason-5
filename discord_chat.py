import discord
import jaconv
import random
import json 
from discord import app_commands
import taiwaBot

TOKEN = 'MTMyMTg2NDkzNTQ0NTM2ODgzMg.Gkesm8.0gSoHoURJ5dHS3RfMHqiEAto5JEMAaecrzbJnY'
CHANNELID =  967834815674077194
intents = discord.Intents.default()
intents.message_content = True

# クライアントの生成
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print('起動しました')


@client.event
async def on_message(message):
    if not message.author.bot:
        channel = client.get_channel(CHANNELID)
        send_message = taiwaBot.taiwa_change(str(message.content))
        await channel.send(send_message)

client.run(TOKEN)
