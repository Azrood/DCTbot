import discord
from discord.ext import commands
from secret import token

bot = commands.Bot(command_prefix='!',help_command=None, description=None)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
@bot.command() 
async def help(ctx): 
    embed = discord.Embed(title="Bot DCTrad", description="Liste des commandes :", color=0xeee657)
    embed.add_field(name="help",value="affiche la liste des commandes",inline=False)
    await ctx.send(embed=embed)
bot.run(token)
