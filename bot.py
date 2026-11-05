import os
import discord
from discord.ext import commands
from groq import Groq

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Groq client (uses your Groq API key from Render)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
        
        if not user_text:
            user_text = "hi"

        try:
            # Generate response using Groq's lightning-fast Llama 3 model
            chat_completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": PERSONA_SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=1.0,
                max_tokens=150
            )
            reply_text = chat_completion.choices[0].message.content
        except Exception as e:
            print(f"DETAILED GROQ ERROR: {e}")
            reply_text = "ou shi... my brain lagged, typeshit gng 💀"

        await message.channel.send(reply_text)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
