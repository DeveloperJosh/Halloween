import discord
import asyncio
import os
from utils.database import db

async def staff_only(ctx):
        e = db.collection.find_one({"_id": ctx.author.id})
        if e["staff"] == True:
            return True
        else:
            return False
