import time

import logging

from discord.embeds import Embed
from discord.ext import commands
from utils.buttons import Joined
from utils.database import db
from config import event_channel, event

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
            msg = await ctx.fetch_message(e['_id'])
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

def setup(bot):
    bot.add_cog(Events(bot=bot))