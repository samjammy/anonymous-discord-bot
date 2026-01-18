import os
import discord
from discord import app_commands

# ===== CONFIG =====
OWNER_ID = 1461686040552017943
LOG_CHANNEL_ID = 1462358263260643429  # <-- replace with your log channel ID

ALLOWED_USERS = {
    1461686040552017943
}
# ==================

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

# -------- /say --------
@client.tree.command(name="say", description="Send an anonymous message")
@app_commands.describe(text="Message to send anonymously")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.defer(ephemeral=True)

    if interaction.user.id not in ALLOWED_USERS:
        await interaction.followup.send(
            "You are not allowed to use this command.",
            ephemeral=True
        )
        return

    try:
        await interaction.channel.send(text)
    except Exception:
        await interaction.followup.send(
            "I don’t have permission to send messages in this channel.",
            ephemeral=True
        )
        return

    # Log usage
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(
            f"📝 **/say used**\n"
            f"User: {interaction.user} (`{interaction.user.id}`)\n"
            f"Channel: {interaction.channel.mention}\n"
            f"Message: `{text}`"
        )

    await interaction.followup.send(
        "Message sent anonymously ✅",
        ephemeral=True
    )

# -------- /allow --------
@client.tree.command(name="allow", description="Allow a user ID to use /say")
@app_commands.describe(user_id="Discord user ID to allow")
async def allow(interaction: discord.Interaction, user_id: str):
    await interaction.response.defer(ephemeral=True)

    if interaction.user.id != OWNER_ID:
        await interaction.followup.send(
            "Only the bot owner can use this command.",
            ephemeral=True
        )
        return

    try:
        uid = int(user_id)
    except ValueError:
        await interaction.followup.send(
            "Invalid user ID.",
            ephemeral=True
        )
        return

    if uid in ALLOWED_USERS:
        await interaction.followup.send(
            "User is already allowed.",
            ephemeral=True
        )
        return

    ALLOWED_USERS.add(uid)

    log_channel = client.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(
            f"✅ **User allowed**\n"
            f"Added by: {interaction.user} (`{interaction.user.id}`)\n"
            f"Allowed User ID: `{uid}`"
        )

    await interaction.followup.send(
        f"User `{uid}` has been allowed to use /say.",
        ephemeral=True
    )

# -------- /allowed --------
@client.tree.command(name="allowed", description="Show allowed user IDs")
async def allowed(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    if interaction.user.id != OWNER_ID:
        await interaction.followup.send(
            "Only the bot owner can view this.",
            ephemeral=True
        )
        return

    users = "\n".join(f"- `{uid}`" for uid in ALLOWED_USERS)

    await interaction.followup.send(
        f"👀 **Allowed Users:**\n{users}",
        ephemeral=True
    )

client.run(os.getenv("BOT_TOKEN"))
