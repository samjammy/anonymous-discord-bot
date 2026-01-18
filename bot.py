import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@slash.slash(name="say", description="Anonymous message")
async def say(ctx: SlashContext, text: str):
    await ctx.defer(hidden=True)

    if ctx.author.id == 886441379654426656:
        await ctx.channel.send(text)
    else:
        await ctx.send("Not allowed", hidden=True)

bot.run(os.getenv("BOT_TOKEN"))
