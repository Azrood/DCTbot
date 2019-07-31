import discord
from discord.ext import commands
from secret import token,dcteam_role_id,dcteam_id

bot = commands.Bot(command_prefix='!',help_command=None, description=None)
client=discord.Client()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.guild=bot.get_guild(dcteam_id) #se lier au serveur à partir de l'ID

@bot.command() 
async def help(ctx): 
    embed = discord.Embed(title="Bot DCTrad", description="Liste des commandes(toutes les commandes doivent être précées du prefix \"!\") :", color=0x0000FF)
    embed.add_field(name="help",value="affiche la liste des commandes",inline=False)
    embed.add_field(name="team",value="assigne le rôle DCTeam au(x) membre(s) mentionné(s)",inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def team(ctx):
    role_dcteam = bot.guild.get_role(dcteam_role_id)
    member_list = ctx.message.mentions #une liste d'objets
    if ctx.author.top_role >= role_dcteam: #on regarde si le plus haut role de l'auteur du message est au dessus du role (ou égal) au role DCT dans la hiérarchie
        for member in member_list:
            await member.add_roles(role_dcteam)
        await ctx.send("Bienvenue dans la Team !")
    else:
        await ctx.send("Bien tenté mais tu n'as pas de pouvoir ici !")
bot.run(token)