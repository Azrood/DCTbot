import discord
from discord.ext import commands
from utils.secret import token,dcteam_role_id,dcteam_id
from utils.tools import get_command_input
from utils.urban import get_top_def
from utils.getcomics import getcomics_top_link
from utils.youtube import youtube_top_link,search_youtube
import asyncio

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
    embed.add_field(name="getcomics",value="recherche dans getcomics les mots-clés entrés",inline=False)
    embed.add_field(name="urban",value="fait une recherche du mot éntré sur Urban Dictionary",inline=False)
    embed.add_field(name="clear",value="efface le nombre de message entré en argument (!clear [nombre])",inline=False)
    embed.add_field(name="recrutement",value="donne le lien des tests de DCTrad",inline = False)
    embed.add_field(name="youtube",value="donne le lien du premier résultat de la recherche",inline = False)
    embed.add_field(name="youtubelist",value="donne une liste de lien cliquables. Syntaxe : !youtubelist [nombre] [recherche]",inline = False)
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
@bot.command()
async def getcomics(ctx):
    user_input = get_command_input(ctx.message.content)
    title,url = getcomics_top_link(user_input)
    embed = discord.Embed(title=f"{title}",description = "cliquez sur le titre pour télécharger votre comic",color=0x882640,url=url)
    await ctx.send(embed=embed)

@bot.command()
async def urban(ctx):
    user_input = get_command_input(ctx.message.content)
    title,meaning,example,search_url = get_top_def(user_input)
    embed = discord.Embed(title=f"Definition of {title}",description = meaning, color=0x00FFFF,url=search_url )
    embed.add_field(name="Example",value=example,inline=False)
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/HMmIAukJm0YaGc2BKYGx5MuDJw8LUbwqZM9BW9oey5I/https/i.imgur.com/VFXr0ID.jpg")
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx):
    role_dcteam = bot.guild.get_role(dcteam_role_id)
    if ctx.author.top_role >= role_dcteam : #on regarde si le plus haut role de l'auteur est supérieur ou égale hiérarchiquement au role DCT
        nbr_msg = int(get_command_input(ctx.message.content))
        messages = await ctx.channel.history(limit=nbr_msg+1).flatten()
        await ctx.channel.delete_messages(messages)
        await ctx.send(content=f"J'ai supprimé {nbr_msg} messages",delete_after=5)
    else:
        await ctx.send(content="Tu n'as pas le pouvoir !")

@bot.command()
async def recrutement(ctx):
    embed=discord.Embed(title="Viens avec nous si tu veux lire",description ="allez n'aies pas peur de cliquer",color=0x0000FF,url="http://www.dctrad.fr/viewforum.php?f=21")
    embed.set_thumbnail(url="http://www.dctrad.fr/ext/planetstyles/flightdeck/store/logodctweb.png")
    await ctx.send(embed=embed)

@bot.command()
async def youtube(ctx):
    user_input=get_command_input(ctx.message.content)
    title,id = youtube_top_link(user_input)
    url=f"https://www.youtube.com/watch?v={id}"
    await ctx.send(content=f"{title}\n{url}")

@bot.command()
async def youtubelist(ctx):
    user_input = get_command_input(ctx.message.content)
    duo = user_input.split(' ', 1)
    number = int(duo[0])
    query = duo[1]
    result = search_youtube(user_input=query,number=number)
    url = "https://www.youtube.com/watch?v="
    embed = discord.Embed(color=0xFF0000)
    embed.set_footer(text="Tapez un nombre pour faire votre choix ou dites \"cancel\" pour annuler")
    for s in result:
        embed.add_field(name=f"{result.index(s)+1}.[{s['title']}]({url}{s['id']})",value=None,inline=False)
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for("message",check=lambda message: message.author == ctx.author,timeout=30)
        if msg.content == "cancel":
            await ctx.send("Annulé !")
        else:
            num = int(msg.content)
            if num > 1 and num <= len(result):
                await ctx.send(content=f"{url}{result[num-1]['id']}")
    except asyncio.TimeoutError:
        await ctx.send("Tu as pris trop de temps pour répondre !")
        
    
bot.run(token)