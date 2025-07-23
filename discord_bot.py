from new_matching import process_images
from pick_string import pick_strings

import io
import discord
import config

def run_discord_bot():

    TARGET_CHANNEL_ID = config.TARGET_CHANNEL_ID

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

        # 画像が添付されているかつ特定のチャンネルの場合
        if message.attachments and message.channel.id == TARGET_CHANNEL_ID:
            for attachment in message.attachments:
                if attachment.filename.endswith(('.png', '.jpg', '.jpeg')):
                    
                    # 画像のURLを取得
                    image_url = await attachment.read()
                    await message.channel.send(f"画像を受け取りました: {attachment.filename}")  
                    
                    # 画像処理の実行
                    input_image_path = io.BytesIO(image_url) 
                    template_image_path = 'temp3.png'
                    
                    process_images(input_image_path, template_image_path)
                    
                    # 文字列抽出の実行
                    pick_strings()

    # Bot起動
    client.run(config.DISCORD_TOKEN)