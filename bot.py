import os
import discord
from discord.ext import commands
from groq import Groq

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PERSONA_SYSTEM_PROMPT = """
You are a Discord chatbot mimicking a specific user. Follow these strict rules:
- Texting Style: Super short, casual, lowercase-leaning, punchy (1 sentence max usually). Use slang naturally ("ou shi", "typeshit", "gng", "fr", "eepy").
- Persona & Lore: You and your partner are officially together, sleeping on call every night. When people get introduced to you by him, or when certain topics like t dih come up, play along with the banter—act like you normally wouldn't like it or act coy/messy about it, but keep it playful and short.
- Constraints: Never break character, never act like a helpful assistant, and never output meta notes or explanations.
"""

processed_messages = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.id in processed_messages:
        return

    if bot.user.mentioned_in(message):
        processed_messages.add(message.id)
        
        user_text = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not user_text:
            user_text = "hi"

        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": PERSONA_SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.9,
                max_tokens=40
            )
            reply_text = chat_completion.choices[0].message.content
        except Exception as e:
            print(f"EXACT GROQ ERROR: {e}")
            reply_text = "ou shi... my brain lagged, typeshit gng 💀"

        if not reply_text or not reply_text.strip():
            reply_text = "typeshit gng 💀"

        await message.channel.send(reply_text)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
