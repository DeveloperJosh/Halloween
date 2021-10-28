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
    @commands.has_permissions(administrator=True)
    async def start(self, ctx):
       embed_start = discord.Embed(title="Halloween", description="The Halloween event is starting on <t:1635656483:D>!", color=0xff8000)
       start = await ctx.send(embed=embed_start)
       await asyncio.sleep(10800)
       embed_started = discord.Embed(title="Halloween", description="The Halloween event has started!", color=0xff8000)
       start.edit(embed=embed_started)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def end(self, ctx):
        new_embed = discord.Embed(title="Halloween", description="Halloween has ended", color=0xff8000)
        await ctx.send(embed=new_embed)

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