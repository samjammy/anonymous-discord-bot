import os
import discord
from discord import app_commands

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.tree.command(name="say", description="Send an anonymous message")
@app_commands.describe(text="Message to send anonymously")
async def say(interaction: discord.Interaction, text: str):
    if interaction.user.id != 1461686040552017943:
        await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )
        return

    await interaction.channel.send(text)
    await interaction.response.send_message(
        "Message sent anonymously ✅",
        ephemeral=True
    )

client.run(os.getenv("BOT_TOKEN"))
