import discord
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
KINDROID_API_KEY = os.getenv("KINDROID_API_KEY")
AI_ID = os.getenv("AI_ID")
API_URL = "https://api.kindroid.ai/v1/send-message"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
      print(f"Nova is online as {client.user}!")

@client.event
async def on_message(message):
      if message.author.bot:
                return
            content = message.content.strip()
    user_message = None
    if message.channel.name == "ai-chat":
              user_message = content
elif content.lower().startswith("!chat "):
        user_message = content[6:].strip()
    if not user_message:
              return
          async with message.channel.typing():
                    try:
                                  response = requests.post(
                                                    API_URL,
                                                    headers={"Authorization": f"Bearer {KINDROID_API_KEY}", "Content-Type": "application/json"},
                                                    json={"ai_id": AI_ID, "message": user_message},
                                                    timeout=30
                                  )
                                  print(f"Status: {response.status_code} | Body: {response.text[:300]}")
                                  if response.status_code == 200:
                                                    data = response.json()
                                                    reply = data.get("reply") or data.get("message") or data.get("response") or data.get("text") or str(data)
                                                    if len(reply) > 2000:
                                                                          reply = reply[:1997] + "..."
                                                                      await message.reply(reply)
                    else:
                                      await message.reply(f"Having trouble right now, try again in a moment!")
except Exception as e:
            print(f"Exception: {e}")
            await message.reply("Connection issue, try again in a moment!")

client.run(BOT_TOKEN)
