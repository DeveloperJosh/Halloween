import asyncio
from datetime import datetime

import logging

import discord
from discord.embeds import Embed
from discord.ext import commands
import os

class Halloween(commands.Cog, description="Halloween"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Halloween is ready')

    @commands.command()
    async def start(self, ctx):
        channel = self.bot.get_channel(903086928285560862)
        await channel.send(f"{ctx.author.mention} has started the Halloween event!")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def end(self, ctx):
       channel = ctx.get_channel(903086928285560862)
       await channel.send(f"{ctx.author.mention} has ended the Halloween event!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.send("Stopping the bot")
        await self.bot.close()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

def setup(bot):
    bot.add_cog(Halloween(bot=bot))