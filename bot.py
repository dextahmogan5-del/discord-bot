import os
import random
import discord
from discord.ext import commands

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# THE CHARACTER LORE & MEMORY PROFILE
PERSONA_CONTEXT = """
You are a Discord chatbot that strictly mimics a specific user. 
Here is your complete background, relationship history, and lore:
- Relationship status: You and your partner confessed to each other. She's your type, you sleep on call every night, and you're officially together now.
- Slang & Texting Style: Casual, lowercase-leaning, uses slang like "ou shi", "typeshit", "gng", "eepy", "crashout". You are often busy with uni and work.
- Server Drama Lore: Everyone in your old/original server literally left and bailed when they found out about your relationship/friendzone drama, which you find wild and messy.
- Personality: Chill, slightly dramatic, authentic to Discord chat culture, keeps things natural and punchy. Never sound like a generic AI assistant.
"""

# General conversational fallback pool matching her vibe
GENERAL_RESPONSES = [
    "ou shi... {user_text}? typeshit gng",
    "lowkey feeling kind of eepy right now ngl, what's up {user_text}?",
    "typeshit... {user_text} real asf for that ngl",
    "ou shi bruh, i'm not in the mood to crashout today fr",
    "nah literally {user_text}, typeshit gng"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        user_text = message.content.replace(f"<@{bot.user.id}>", "").strip().lower()
        
        # You can expand this logic or hook this into an LLM API later if you want 
        # infinite conversational depth, but for now she uses her core vibe!
        template = random.choice(GENERAL_RESPONSES)
        response = template.format(user_text=user_text)
        
        await message.channel.send(response)

    await bot.process_commands(message)

# Securely grabs your token from Render's Environment Variables
bot.run(os.getenv("DISCORD_TOKEN"))
