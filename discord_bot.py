import discord
import config
import random

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Bot起動時に呼び出される関数
@client.event
async def on_ready():
    print("Ready!")

# メッセージの検知
@client.event
async def on_message(message):
    # 自身が送信したメッセージには反応しない
    if message.author == client.user:
        return

    # 画像が添付されている場合
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                # 画像のURLを取得
                image_url = attachment.url
                await message.channel.send(f"画像を受け取りました: {image_url}")   

# Bot起動
client.run(config.DISCORD_TOKEN)
