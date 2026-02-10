from flask import Flask
import os
import threading

app = Flask("")

@app.route("/")
def home():
    return "Bot online"

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run).start()

import re
import requests
import discord
import os
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
URL = "https://mcpedl.org/downloading/"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def get_latest_version():
    html = requests.get(URL, timeout=10).text

    match = re.search(
        r'font-weight: 800;">MCPE ([0-9]+\.[0-9]+\.[0-9]+)<span style="font-weight: 400;"> \([^)]*Latest Release\)',
        html
    )

    if not match:
        return None

    version = match.group(1)
    version_dash = version.replace(".", "-")

    download_url = (
        f"https://mcpe-planet.com/wp-content/uploads/version/"
        f"minecraft-{version_dash}-music.apk"
    )

    return version, download_url


@tree.command(name="minecraft", description="Get latest Minecraft Bedrock download")
async def minecraft(interaction: discord.Interaction):
    await interaction.response.defer()

    data = get_latest_version()

    if not data:
        await interaction.followup.send("Não foi possível obter o minecraft")
        return

    version, download_url = data

    embed = discord.Embed(
        title="Minecraft Download",
        color=0x00FF00
    )
    
    embed.set_thumbnail(
    url="https://cdn.discordapp.com/attachments/1446641527769137376/1470621012621263041/Minecraft.webp?ex=698bf60c&is=698aa48c&hm=0cb4b6a1381e3fb8dca0cb65e5c43a45e4de0da40cc27089b65d12cd881fcf4e&"
    )

    embed.description = (
        "**Informations**\n"
        f"Version: `{version}`\n\n"
        "**Downloads**\n"
        f"[Download]({download_url})"
    )

    await interaction.followup.send(embed=embed)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot online - {client.user}")


client.run(TOKEN)
