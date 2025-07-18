from new_matching import process_images
from pick_string import pick_strings

import io
import discord
import config
import random

if __name__ == "__main__":

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
                    image_url = await attachment.read()
                    await message.channel.send(f"画像を受け取りました: {attachment.filename}")  
                    
                    # 画像処理の実行
                    input_image_path = io.BytesIO(image_url) 
                    template_image_path = 'temp3.png'
                    
                    input_color, template_bin, input_bin, cropped_match = process_images(input_image_path, template_image_path)
                    
                    # 文字列抽出の実行
                    pick_strings()

    # Bot起動
    client.run(config.DISCORD_TOKEN)