import os
import random
import discord
from discord.ext import commands

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# A pool of varied responses matching her exact slang, vibe, and lore
RESPONSE_POOL = [
    "ou shi... {user_text}? typeshit gng, everyone really bailed on the server just cause of our whole drama lmao 😭",
    "gng rn? {user_text} got me feeling so eepy after dealing with everyone dipping from the server over the drama fr 💀",
    "typeshit... {user_text}? honestly wild how everyone left the server the second they found out, like y'all are so dramatic smh",
    "ou shi {user_text}, i'm lowkey not in the mood to crashout today especially after everyone abandoning the server over our whole situation lmao",
    "typeshit gng... {user_text}? wild how everyone cleared out of the server like that 😭"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        user_text = message.content.replace(f"<@{bot.user.id}>", "").strip()
        
        # Randomly picks a different response style each time while keeping her vibe
        template = random.choice(RESPONSE_POOL)
        response = template.format(user_text=user_text)
        
        await message.channel.send(response)

    await bot.process_commands(message)

# Securely grabs your token from Render's Environment Variables
bot.run(os.getenv("DISCORD_TOKEN"))
