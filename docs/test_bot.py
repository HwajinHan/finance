import os
import discord
from dotenv import load_dotenv

# .env 파일에서 비밀 키 불러오기
load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ 새 토큰으로 안전하게 로그인 완료: {client.user.name}")

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content == "!안녕":
        await message.reply("보안 처리된 봇이 정상 작동 중입니다! 🤖")

client.run(BOT_TOKEN)