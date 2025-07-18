from dotenv import load_dotenv
load_dotenv()

import os
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))