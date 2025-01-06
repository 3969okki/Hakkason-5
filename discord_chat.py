import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.channel import VoiceChannel
from discord.player import FFmpegPCMAudio
import taiwaBot
import transcription
import asyncio

TOKEN = 'MTMyMTg2NDkzNTQ0NTM2ODgzMg.Gkesm8.0gSoHoURJ5dHS3RfMHqiEAto5JEMAaecrzbJnY'
CHANNELID = 967834815674077194
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'{client.user}がログインしました')
    try:
        await tree.sync()  # スラッシュコマンドを同期
        print("スラッシュコマンドが同期されました")
    except Exception as e:
        print(f"コマンド同期エラー: {e}")


async def get_sounds():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, transcription.get_sounds)

@tasks.loop(seconds=9)  # １０秒ごとに実行
async def periodic_task():
    string = await get_sounds()
    if string:  # stringが空でない場合のみ音声再生
        play_voice(string)

@tree.command(name='change_voice', description='You can change girlfriend voice')
async def change_voice(interaction: discord.Interaction, voice_num: str):
    taiwaBot.speaker = voice_num
    # 応答メッセージを返す
    await interaction.response.send_message(f"声を {voice_num} に変更しました。")

@tree.command(name='change_chara', description='You can change girlfriend character')
async def change_chara(interaction: discord.Interaction, want_character: str):

    taiwaBot.giri_model = want_character
    taiwaBot.chat.send_message(taiwaBot.giri_model)
    # 応答メッセージを返す
    await interaction.response.send_message(f"キャラクターを {want_character} に変更しました。")

@tree.command(name='change_speak_speed', description='You can change girlfriend speak speed(0.5~2.0)')
async def change_speed(interaction: discord.Interaction, want_speed: str):
    taiwaBot.speed = want_speed
    # 応答メッセージを返す
    await interaction.response.send_message(f"対話速度をを {want_speed} に変更しました。")

@tree.command(name='q', description='please question')
async def question(interaction: discord.Interaction, your_question: str):
    await interaction.response.defer()
    ans = taiwaBot.question(your_question)
    for chunk in ans:
        await interaction.followup.send(chunk)


# `on_message` は一度だけ定義
@client.event
async def on_message(message):
    global voiceChannel

    # ボットのメッセージには反応しない
    if message.author.bot:
        return

    # メッセージに応じて接続/切断を行う
    if message.content == '!connect' and message.author.voice:
        voiceChannel = await message.author.voice.channel.connect()
        await message.channel.send('読み上げBotが参加しました')
        periodic_task.start()
        return
    elif message.content == '!disconnect' and voiceChannel:
        voiceChannel.stop()
        await message.channel.send('読み上げBotが退出しました')
        await voiceChannel.disconnect()
        periodic_task.stop()
        return
    else:
        await message.channel.send(taiwaBot.text_taiwa(message))
        

def play_voice(message):
    if voiceChannel.is_playing():  # すでに音声が再生されていないか確認
        return
    text = taiwaBot.taiwa_change(str(message))
    voiceChannel.play(FFmpegPCMAudio("voicevox_output.wav"))

client.run(TOKEN)
