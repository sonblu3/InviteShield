import discord
import re
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_ROLE_IDS = [1351644934981029898]
ALLOWED_CHANNEL_IDS = [12345]
LOG_CHANNEL_ID = 1515266893710360649

discord_link_pattern = re.compile(
    r"(https?:\/\/)?(www\.)?(discord\.gg|discord\.com\/invite)\/\S+",
    re.IGNORECASE
)

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="for invite links"
    ))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.guild_permissions.administrator:
        return

    if any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
        return

    if message.channel.id in ALLOWED_CHANNEL_IDS:
        return

    if discord_link_pattern.search(message.content):
        await message.delete()

        warn = await message.channel.send(
            f"{message.author.mention} links are not allowed here."
        )
        await warn.delete(delay=5)

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"Link removed\nUser: {message.author}\nChannel: {message.channel}\nMessage: {message.content}"
            )

    await bot.process_commands(message)

bot.run(TOKEN)
