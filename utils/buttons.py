import discord
from utils.database import db

class Joined(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # this will probably not be used
    @discord.ui.button(label="Join", style=discord.ButtonStyle.blurple, custom_id="join")
    async def join(self, button, interaction):
        if db.collection.find_one({'_user': interaction.message.author.id}):
            await interaction.response.send_message("You are aready in event.", ephemeral=True)

        else:
            db.collection.insert_one({'_user': interaction.message.author.id})
            await interaction.response.send_message("You have been added to the event.", ephemeral=True)
