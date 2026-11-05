import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands
from openai import OpenAI

# 1. Dummy web server to satisfy Render's Free Web Service port requirement
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# 2. Discord & OpenRouter Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

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
            # Using an explicitly free model tag on OpenRouter
            completion = client.chat.completions.create(
                model="cognitivecomputations/dolphin-mixtral-8x7b:free",
                messages=[
                    {"role": "system", "content": PERSONA_SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.9,
                max_tokens=40
            )
            reply_text = completion.choices[0].message.content
        except Exception as e:
            # THIS WILL PRINT THE EXACT ERROR IN YOUR RENDER LOGS
            print(f"OPENROUTER ERROR: {repr(e)}")
            reply_text = f"err: {str(e)[:45]}"

        if not reply_text or not reply_text.strip():
            reply_text = "err: empty"

        await message.channel.send(reply_text)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
