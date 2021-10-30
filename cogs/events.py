import time

import logging

from discord.embeds import Embed
from discord.ext import commands
from utils.buttons import Joined
from utils.database import db
from config import event_channel, event
from utils.message import wait_for_msg

class Events(commands.Cog, description="Events"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Joined())
        logging.info('Events is ready')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def start(self, ctx):
        e = db.collection.find_one({"_status": "on"})

        if e is None:
          channel = self.bot.get_channel(event_channel)
          embed = Embed(title=f"{event}", description=f"{event} event is starting soon", color=0xFF0000)
          msg = await channel.send(embed=embed)
          await ctx.reply("Event started")
          db.collection.insert_one({"_id": msg.id, "_status": "on", "start":  time.time()})

        else:
            await ctx.send(f"{event} was started <t:{int(e['start'])}:R>")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def end(self, ctx):
        e = db.collection.find_one({"_status": "on"})

        if e is None:
          await ctx.send(f"{event} event is not started!")

        else:
            e = db.collection.find_one({"_status": "on"})

            embed = Embed(title=f"{event}", description=f"{event} event has ended!", color=0xFF0000)
            channel = self.bot.get_channel(event_channel)  
            msg = await channel.fetch_message(e['_id'])
            await msg.edit(embed=embed)
            await ctx.send(f"{event} event has ended!")     
            db.collection.delete_one({"_status": "on"})

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.send("Stopping the bot")
        await self.bot.close()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def apply(self, ctx):
        """Apply for developer"""
        main_message = await ctx.send("Answer these questions: Do you know python, Why should we pick you our the others, have you worked with react before?")
        users_message = await wait_for_msg(ctx, 300, main_message)

        if users_message is None:
            return

        else:
            channel = self.bot.get_channel(888417066586112031)
            embed = Embed(title="Application", description=f"Sent by {ctx.author.name}\n {users_message.content}", color=0xFF0000)
            msg = await channel.send(embed=embed)
            await users_message.delete()
            await ctx.send("Application sent")

def setup(bot):
    bot.add_cog(Events(bot=bot))