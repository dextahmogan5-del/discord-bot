import asyncio
import os
import random
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

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

# 2. Discord Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Combined general response bank (your lines + extra variety)
DEFAULT_RESPONSES = [
    "typeshit gng 💀",
    "ou shi fr",
    "nah ur tweaking",
    "eepy af rn ngl",
    "im waiting for him to call",
    "lets see how it goes",
    "im kinda pissed",
    "that sounds sad",
    "okie thanks",
    "typeshit",
    "bro what are you on about",
    "real",
    "so true bestie",
    "nah literally",
    "who let bro cook",
    "💀💀",
    "smh",
    "ong",
    "fr fr",
    "bro is baffling me",
    "you're actually insane",
    "wild statement",
    "couldn't be me",
    "nah chill",
    "ain't no way",
    "bro really said that 😭",
]

# Combined keyword responses (your exact lines + extra options)
KEYWORD_RESPONSES = {
    "hello": ["yo", "sup gng", "wassup", ":p", "oh hey"],
    "hi": ["yo", "sup", "hey", "yeeee"],
    "t dih": [
        "ALL HAIL TO T DIH 🙌", 
        "HELL YEAHH", 
        "im not sure if its my tdih or freddys tdih ❤️", 
        "I GOT AN ENORMOUS DIH 🔥", 
        "OOOOO HELL YEHA",
        "bro wtf 💀",
        "nah you're wild for bringing that up",
        "coy af rn ngl",
    ],
    "tdih": [
        "ALL HAIL TO T DIH 🙌", 
        "HELL YEAHH", 
        "im not sure if its my tdih or freddys tdih ❤️", 
        "I GOT AN ENORMOUS DIH 🔥", 
        "OOOOO HELL YEHA",
        "bro wtf 💀",
        "nah you're wild for bringing that up",
        "coy af rn ngl",
    ],
    "t-dih": [
        "ALL HAIL TO T DIH 🙌", 
        "HELL YEAHH", 
        "im not sure if its my tdih or freddys tdih ❤️", 
        "I GOT AN ENORMOUS DIH 🔥", 
        "OOOOO HELL YEHA",
        "bro wtf 💀",
        "nah you're wild for bringing that up",
        "coy af rn ngl",
    ],
    "sleep": [
        "nah sleeping on call rn", 
        "eepy as hell", 
        "we jus watching netflix and chilling",
        "we literally stay on call every night wdym"
    ],
    "call": [
        "im waiting for him to call", 
        "sleeping on call rn",
        "on call rn 🥱"
    ],
    "type": [
        "she's jus my type but she's my fren get it", 
        "typeshit 😭"
    ],
    "babe": [
        "talked to my babe today", 
        "im not in mood to crashout"
    ],
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        raw_text = message.content.replace(f"<@{bot.user.id}>", "").strip().lower()
        
        # Strips spaces and hyphens so tdih, t-dih, and t dih are all recognized identically
        normalized_text = re.sub(r'[\s\-]+', '', raw_text)
        
        reply_text = None
        for keyword, responses in KEYWORD_RESPONSES.items():
            norm_keyword = keyword.replace(" ", "").replace("-", "")
            if norm_keyword in normalized_text or keyword in raw_text:
                reply_text = random.choice(responses)
                break
        
        # Fallback to random general line if no keyword triggered
        if not reply_text:
            reply_text = random.choice(DEFAULT_RESPONSES)

        # Simulates typing status and a natural delay (between 1.0 and 2.2 seconds)
        async with message.channel.typing():
            await asyncio.sleep(random.uniform(1.0, 2.2))

        await message.channel.send(reply_text)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
