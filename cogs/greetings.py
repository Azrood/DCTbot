import asyncio
import random
from utils.constants import greeting_list

import discord
from discord.ext import commands, tasks

class Greetings(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.morning_greeting.start() # pylint: disable=no-member

    @tasks.loop(seconds=24)
    async def morning_greeting(self):
        """Send greetings in the morning."""
        channel_general = discord.utils.get(self.bot.guild.text_channels, name='general')
        greeting = random.choice(greeting_list)
       
        await channel_general.send(content=greeting)

    @morning_greeting.before_loop
    async def before_morning_greeting(self):
        """Intiliaze morning_greeting loop."""
        await self.bot.wait_until_ready()
        await asyncio.sleep(delay=3) # wait 10 hours after boot