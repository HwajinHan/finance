import discord

BOT_TOKEN = "MTU1NDczMDcwNTkxMTY3NzAwMA.GanoqM.ajxZmEQ2B76G2iMeI4GV8uYN7esXWJSNCGQ1gg"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ 디스코드 봇 온라인: {client.user.name}")
    print("디스코드 방에서 '!안녕'을 쳐보세요.")

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content == "!안녕":
        await message.reply("안녕하세요! 자산 관리 봇이 준비되었습니다. 🤖")

client.run(BOT_TOKEN)