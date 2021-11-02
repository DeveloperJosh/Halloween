import discord
from discord.enums import Status
from discord.ext import commands
import asyncio
import random
import string
import datetime
import time
from utils.checks import staff_only
from utils.database import db

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Staff is ready')

    @commands.command(name="register", aliases=["reg"])
    async def register(self, ctx):
        e = db.collection.find_one({"_id": ctx.author.id})
        if e is None:
            db.collection.insert_one({"_id": ctx.author.id, "staff": False, "registered": True, "last_seen": datetime.datetime.utcnow()})
            await ctx.send("You have been registered as a user.")
        else:
            await ctx.send("You are already registered.")

    @commands.command(name="force-register")
    @commands.is_owner()
    async def force_register(self, ctx, user: discord.Member):
        e = db.collection.find_one({"_id": user.id})
        if e is None:
            db.collection.insert_one({"_id": user.id, "staff": False, "registered": True, "last_seen": datetime.datetime.utcnow()})
            await ctx.send("You have been registered as a user.")
        else:
            await ctx.send("You are already registered.")

    @commands.command(name="unregister", aliases=["unreg"])
    async def unregister(self, ctx):
        e = db.collection.find_one({"_id": ctx.author.id})
        if e is not None:
            db.collection.delete_one({"_id": ctx.author.id})
            await ctx.send("You have been unregistered.")
        else:
            await ctx.send("You are not registered.")

    @commands.command(name="add", aliases=["add-staff"])
    @commands.is_owner()
    async def staff(self, ctx, user: discord.Member):
        e = db.collection.find_one({"_id": user.id})
        if e['staff'] is False:
            db.collection.update_one({"_id": user.id}, {"$set": {"staff": True}})
            await ctx.send(f"{user.name} has been added to the staff list.")
        
        elif e is None:
            await ctx.send("That user is not registered.")
        
        else:
            await ctx.send(f"{user.name} is already a staff member.")

    @commands.command(name="remove", aliases=["remove-staff"])
    @commands.is_owner()
    async def remove(self, ctx, user: discord.Member):
        e = db.collection.find_one({"_id": user.id})
        if e['staff'] is True:
            db.collection.update_one({"_id": user.id}, {"$set": {"staff": False}})
            await ctx.send(f"{user.name} has been removed from the staff list.")
        
        elif e is None:
            await ctx.send("That user is not registered.")
        
        else:
            await ctx.send(f"{user.name} is not a staff member.")

    @commands.command(name="staff-list", aliases=["stafflist"])
    @commands.check(staff_only)
    async def staff_list(self, ctx):
        e = db.collection.find({"staff": True})
        if e.count() == 0:
            await ctx.send("There are no staff members.")
        else:
            embed = discord.Embed(title=f"Staff Members", description=f"\n".join([f"**{self.bot.get_user(data.get('_id', '1234'))}** - `{data.get('_id', '1234')}`" for data in e]), color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command(name="user-list", aliases=["userlist"])
    @commands.check(staff_only)
    async def user_list(self, ctx):
        e = db.collection.find({"registered": True})
        if e.count() == 0:
            await ctx.send("There are no users.")
        else:
            embed = discord.Embed(title=f"Registered Users", description=f"\n".join([f"**{self.bot.get_user(data.get('_id', '1234'))}** - `{data.get('_id', '1234')}`" for data in e]), color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    async def report(self, ctx, user: discord.Member, *, reason):
            report_id = id_generator()
            embed = discord.Embed(title=f"{ctx.author.name} has made a report", description=f"User: {user.name}\nId: {user.id}\nReason: {reason}", color=0x00ff00)
            db.collection.insert_one({"_id": report_id, "user": user.id, "author": ctx.author.id, "reason": reason, "Status": "Open", "date": datetime.datetime.utcnow()})
            embed.set_footer(text=f"Report Id: {report_id}")
            channel = self.bot.get_channel(903090469368647740)
            await channel.send(embed=embed)

    @commands.command()
    async def reportlist(self, ctx):
        e = db.collection.find({"Status": "Open"})
        if e.count() == 0:
            await ctx.send("There are no reports.")
        else:
            embed = discord.Embed(title=f"Open Reports", description=f"\n".join([f"**{self.bot.get_user(data.get('user', '1234'))}** - `{data.get('reason', 'none')}` - Id {data.get('_id', 'none')}" for data in e]), color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    async def resolve(self, ctx, report_id):
        e = db.collection.find_one({"_id": report_id})
        if e is None:
            await ctx.send("That report does not exist.")
        else:
            db.collection.update_one({"_id": report_id}, {"$set": {"Status": "Closed"}})
            await ctx.send("Report has been resolved.")

    @commands.command()
    async def reportinfo(self, ctx, report_id):
        e = db.collection.find_one({"_id": report_id})
        if e is None:
            await ctx.send("That report does not exist.")
        else:
            embed = discord.Embed(title=f"Report Info", description=f"User: {self.bot.get_user(e.get('user', '1234'))}\nId: {e.get('user', '1234')}\nReason: {e.get('reason', 'none')}\nStatus: {e.get('Status', 'none')}\nDate: {e.get('date', 'none')}", color=0x00ff00)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Staff(bot))