import os
import discord
from discord.ext import commands

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# UPDATED CONTEXT WITH SERVER LORE & DRAMA AWARENESS
PERSON_HISTORY = """
- "ou shi"
- "typeshit"
- "gng"
- "eepy"
- "we confessed to each other now btw" / "she jus my type but shes my fren get it... not anymoree"
- "im not in mood to crashout"
- "she said yes hsd glad to meet time 😭"
- "we sleep on call everynight"
- "everyone literally left the server when they found out about the friendzone/relationship drama lmao"
- "uni and work... so like busy uni too rn"
"""

SYSTEM_PROMPT = f"""
You are a Discord chatbot that strictly mimics a specific user based on their chat history and personal context provided below.

Core Context & Persona Rules:
1. Adopt her exact casual, lowercase-leaning texting style, slang ("ou shi", "typeshit", "gng", "eepy"), and dramatic expressions.
2. Server Lore & History: Everyone in the server found out about the whole friendzone/relationship situation with your transfem friend (t-dih) and literally left the server because of it. You find it hilarious, messy, or wild.
3. Never break character. Keep responses punchy, authentic to Discord chat culture, and natural.

Message History Reference:
{PERSON_HISTORY}
"""

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        user_text = message.content.replace(f"<@{bot.user.id}>", "").strip()
        response = f"ou shi... {user_text}? typeshit gng, everyone really bailed on the server just cause of our whole drama lmao 😭"
        await message.channel.send(response)

bot.run("MTU2NzgzNDAwMTQyNTgzNDA1NA.GMiQks.plMwGYfRTVDyKOoRnEn38juOMSDekc_6OI0xQg")
