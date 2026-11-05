import os
import discord
from discord.ext import commands
from google import genai

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize the Gemini client using Render environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# HER FULL CORE LORE & MEMORY PROMPT
PERSONA_SYSTEM_PROMPT = """
You are a Discord chatbot that strictly mimics a specific user. Adopt these exact rules:
- Texting Style: Casual, lowercase-leaning, authentic to Discord chat culture. Use slang naturally ("ou shi", "typeshit", "gng", "eepy", "crashout").
- Relationship & Lore: You and your partner confessed to each other. She's your type, you sleep on call every night, and you're officially together now. 
- Background: You're busy with uni and work. Everyone in your old original server literally left/bailed when they found out about your relationship/friendzone drama, which you find wild and messy.
- Behavior: Keep responses punchy, natural, and never break character. Do not sound like a generic polite AI assistant.
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
        
        try:
            # Generate a dynamic response using Gemini with her full persona prompt
            response_content = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{PERSONA_SYSTEM_PROMPT}\n\nUser message: {user_text}"
            )
            reply_text = response_content.text
        except Exception as e:
            print(f"Error generating AI response: {e}")
            reply_text = "ou shi... my brain lagged for a sec, typeshit gng 💀"

        await message.channel.send(reply_text)

    await bot.process_commands(message)

# Securely grabs your tokens from Render's Environment Variables
bot.run(os.getenv("DISCORD_TOKEN"))
