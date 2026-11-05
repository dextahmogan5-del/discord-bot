import os
import discord
from discord.ext import commands
from groq import Groq

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Groq client using your GROQ_API_KEY environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# HER FULL CORE LORE & MEMORY PROMPT
PERSONA_SYSTEM_PROMPT = """
You are a Discord chatbot that strictly mimics a specific user. Adopt these exact rules:
- Texting Style: Casual, lowercase-leaning, authentic to Discord chat culture. Use slang naturally ("ou shi", "typeshit", "gng", "eepy", "crashout").
- Relationship & Lore: You and your partner confessed to each other. She's your type, you sleep on call every night, and you're officially together now. 
- Background: You're busy with uni and work. Everyone in your old original server literally left/bailed when they found out about your relationship/friendzone drama, which you find wild and messy.
- Behavior: Keep responses punchy, natural, and never break character. Do not sound like a generic polite AI assistant.
"""

# Track processed message IDs to prevent double replies
processed_messages = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Prevent processing the same message twice if event triggers in duplicates
    if message.id in processed_messages:
        return

    # Check if the bot was mentioned
    if bot.user.mentioned_in(message):
        processed_messages.add(message.id)
        
        user_text = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not user_text:
            user_text = "hi"

        try:
            # Using Groq's active production model ID
            chat_completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": PERSONA_SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=1.0,
                max_tokens=150
            )
            reply_text = chat_completion.choices[0].message.content
        except Exception as e:
            print(f"EXACT GROQ ERROR: {e}")
            reply_text = f"err: {e}"

        await message.channel.send(reply_text)

    await bot.process_commands(message)

# Securely grabs your bot token from Render's Environment Variables
bot.run(os.getenv("DISCORD_TOKEN"))
