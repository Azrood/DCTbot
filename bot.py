#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import os
import sys
import discord
import asyncio
import random
from discord.ext import commands, tasks
from utils.secret import token, dcteam_role_id, dcteam_id, modo_role_id, dcteam_category_id, admin_id, nsfw_channel_id, admin_role  # noqa: E501
from utils.tools import string_is_int
from utils.urban import UrbanSearch
from utils.getcomics import getcomics_top_link
from utils.youtube import youtube_top_link, search_youtube, get_youtube_url
from utils.comicsblog import get_comicsblog
from utils.google import search_google, google_top_link
from utils.gif_json import GifJson
from utils.bonjourmadame import latest_madame
from utils.header import get_header, get_monthly_url
from utils.reddit import reddit_nsfw
import datetime 

bot = commands.Bot(command_prefix='!', help_command=None, description=None, case_insensitive=True)

urban_logo = "https://images-ext-2.discordapp.net/external/HMmIAukJm0YaGc2BKYGx5MuDJw8LUbwqZM9BW9oey5I/https/i.imgur.com/VFXr0ID.jpg"  # noqa: E501

dctradlogo = "http://www.dctrad.fr/ext/planetstyles/flightdeck/store/logodctweb.png"  # noqa: E501

dctrad_recru = "http://www.dctrad.fr/viewforum.php?f=21"

snap_url = "https://media.tenor.com/images/8d7d2e757f934793bb4154cede8a4afa/tenor.gif"  # noqa: E501

helps = [
    {'name': 'help', 'value': 'affiche la liste des commandes'},
    {'name': 'gif help', 'value': 'affiche la liste des gifs'},
    {'name': 'poke help', 'value': 'affiche la liste des cartes'},
    {'name': 'getcomics', 'value': 'recherche dans getcomics les mots-clés entrés'},  # noqa: E501
    {'name': 'urban', 'value': 'fait une recherche du mot entré sur Urban Dictionary'},  # noqa: E501
    {'name': 'recrutement', 'value': 'donne le lien des tests de DCTrad'},
    {'name': 'timer', 'value': 'minuteur qui notifie le user après X secondes\n Syntaxe : !timer [nombre (secondes)] [rappel]\n Exemple: !timer 3600 organiser mes dossiers'},  # noqa: E501
    {'name': 'youtube', 'value': 'donne le lien du premier résultat de la recherche\n Supprime le lien si l\'utilisateur supprime son message'},  # noqa: E501
    {'name': 'youtubelist', 'value': 'donne une liste de liens cliquables.\n Syntaxe : !youtubelist [nombre] [recherche]'},  # noqa: E501
    {'name': 'comicsblog', 'value': 'donne les X derniers articles de comicsblog\n (syntaxe : !comicsblog [numero])'},  # noqa: E501
    {'name': 'google', 'value': 'donne le premier lien de la recherche google avec les mots-clés saisis'},  # noqa: E501
    {'name': 'googlelist', 'value': 'donne une liste des X premiers liens de la recherche google\n Syntaxe : !googlelist [numero] [mots-clés] \nExemple : !googlelist 3 the final countdown'},  # noqa: E501
    {'name': 'roulette', 'value': '1/6 chance de se faire kick, la roulette russe avec le bon Colt !'},  # noqa: E501
    {'name': 'choose', 'value': "choisit aléatoiremement parmi plusieurs arguments \n Syntaxe : !choose arg1 arg2 \"phrase avec plusieurs mots\" (si vous voulez des choix avec plusieurs mots, mettez vos choix entre \"\" comme pâr exemple \n !choose \"manger chinois\" \"manger italien \" \" manger quelqu'un \" ) "},  # noqa: E501
    {"name": "coinflip", 'value': "fais un lancer de pile ou face"},
    {'name': 'say', 'value': "répète ce qui est entré et supprime le message du user"}  # noqa: E501
    ]
help_team = [
    {'name': 'team', 'value': 'assigne le rôle DCTeam au(x) membre(s) mentionné(s)'},  # noqa: E501
    {'name': 'clear', 'value': 'efface le nombre de message entré en argument (!clear [nombre])'}  # noqa: E501
    ]
help_above = [
    {'name': 'kick', 'value': 'kick la(les) personne(s) mentionnée(s)\n (syntaxe : !kick [@membre] (optionel)[@membre2]...'},  # noqa: E501
    {'name': 'ban', 'value': 'bannit le(s) user(s) mentionné(s)\n Syntaxe : !ban [@membre1][@membre2]....'}  # noqa: E501
    ]

poke_help="azrod\nbane\nrun\nsergei\n" #see comment in line 509

dir_path = os.path.dirname(os.path.realpath(__file__))
my_giflist = GifJson("gifs.json")


@bot.event
async def on_ready():
    """Log in Discord."""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.guild = bot.get_guild(dcteam_id)  # se lier au serveur à partir de l'ID
    bot.role_dcteam = bot.guild.get_role(dcteam_role_id)
    bot.role_modo = bot.guild.get_role(modo_role_id)


@bot.command()
async def help(ctx):
    """Display available commands."""
    embed = discord.Embed(title="Page 1/2, utilisez les flèches en réaction pour naviguer", description="Liste des commandes(toutes les commandes doivent être précédées du prefix \"!\") :", color=0x0000FF)  # noqa: E501
    embed_2 = discord.Embed(title="Page 2/2, utilisez les flèches en réaction pour naviguer", description="Liste des commandes(toutes les commandes doivent être précédées du prefix \"!\") :", color=0x0000FF)  # noqa: E501
    for s in helps:
        if len(embed.fields) < 10:
            embed.add_field(name=s['name'], value=s['value'], inline=False)
        else:
            embed_2.add_field(name=s['name'], value=s['value'], inline=False)
    if ctx.author.top_role >= bot.role_dcteam:
        for h in help_team:
            embed_2.add_field(name=h['name'], value=h['value'], inline=False)
    if ctx.author.top_role >= bot.role_modo:
        for h in help_above:
            embed_2.add_field(name=h['name'], value=h['value'], inline=False)
    if ctx.channel.category_id == dcteam_category_id:
        embed.add_field(name='nsfw', value="affiche une image nsfw", inline=False)  # noqa: E501
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("\U000025c0")
    await msg.add_reaction("\U000025b6")

    @tasks.loop(seconds=2)
    async def helperloop():
        def check(reaction, user):
            return (ctx.author == user
                    and str(reaction.emoji) in ["\U000025b6", "\U000025c0"]
                    and msg.id == reaction.message.id)
        reaction, user = await bot.wait_for("reaction_add", check=check, timeout=60)  # noqa: E501
        if str(reaction.emoji) == "\U000025c0":
            await msg.edit(embed=embed)
        elif str(reaction.emoji) == "\U000025b6":
            await msg.edit(embed=embed_2)
        else:
            return None
        await reaction.remove(user)
    await msg.delete(delay=60)
    helperloop.start()


@bot.command()
async def team(ctx):
    """Give 'team' role to user list."""
    member_list = ctx.message.mentions  # une liste d'objets
    # on regarde si le plus haut role de l'auteur du message est au dessus
    # du role (ou égal) au role DCT dans la hiérarchie
    counter = 0
    if ctx.author.top_role >= bot.role_dcteam:
        if not member_list:
            pass
        else:
            for member in member_list:
                if bot.role_dcteam in member.roles:  # le counter c'est pour voir si tous les membres mentionnés  # noqa: E501
                    counter += 1
                await member.add_roles(bot.role_dcteam)  # sont dans la team, alors on n'affiche pas le message de bienvenue  # noqa: E501
            if counter == len(member_list):
                return None
            await ctx.send(content="Bienvenue dans la Team !")
    else:
        await ctx.send(content="Bien tenté mais tu n'as pas de pouvoir ici !")


@bot.command()
async def getcomics(ctx, *, user_input):
    """Send direct download link for getcomics search result."""
    title, url = getcomics_top_link(user_input)
    embed = discord.Embed(title=f"{title}",
                          description="cliquez sur le titre pour télécharger votre comic",  # noqa: E501
                          color=0x882640, url=url)
    await ctx.send(embed=embed)


@bot.command()
async def urban(ctx, *, user_input):
    """Send definition of user input on Urban Dictionary."""
    # create object urban of class Urban
    urban = UrbanSearch(user_input)
    if urban.valid:
        title, meaning, example, search_url = urban.get_top_def()
        embed = discord.Embed(title=f"Definition of {title}",
                              description=meaning, color=0x00FFFF,
                              url=search_url)
        embed.add_field(name="Example", value=example, inline=False)
        embed.set_thumbnail(url=urban_logo)
    else:
        embed = discord.Embed(title=f"Definition of {user_input} doesn't exist")  # noqa: E501
    await ctx.send(embed=embed)


@bot.command()
async def clear(ctx, number):
    """Clear n messages."""
    # on regarde si le plus haut role de l'auteur est supérieur
    # ou égal hiérarchiquement au role DCT
    if ctx.author.top_role >= bot.role_dcteam:
        nbr_msg = int(number)
        messages = await ctx.channel.history(limit=nbr_msg + 1).flatten()
        await ctx.channel.delete_messages(messages)
        await ctx.send(content=f"J'ai supprimé {nbr_msg} messages",
                       delete_after=5)
    else:
        await ctx.send(content=f"Tu n'as pas le pouvoir{ctx.author.mention} !")


@bot.command()
async def recrutement(ctx):
    """Send 'recrutement' topic url."""
    embed = discord.Embed(title="Rejoins le team DCTrad !",
                          description="allez n'aies pas peur de cliquer et deviens un héros !",  # noqa: E501
                          color=0x0000FF, url=dctrad_recru)
    embed.set_thumbnail(url=dctradlogo)
    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx, *, user_input):
    """Send first Youtube search result."""
    title, url = youtube_top_link(user_input.lower())
    link = await ctx.send(content=f"{title}\n{url}")

    def check(message):
        return message == ctx.message
    await bot.wait_for("message_delete", check=check, timeout=1200)
    await link.delete(delay=None)


@bot.command()
async def youtubelist(ctx, num, *, query):
    """Send n Youtube search results."""
    number = int(num)
    if number > 10:
        number = 10
    result = search_youtube(user_input=query, number=number)
    embed = discord.Embed(color=0xFF0000)
    embed.set_footer(text="Tapez un nombre pour faire votre choix "
                          "ou dites \"cancel\" pour annuler")
    for s in result:
        url = get_youtube_url(s)
        embed.add_field(name=f"{result.index(s)+1}.{s['type']}",
                        value=f"[{s['title']}]({url})", inline=False)
    self_message = await ctx.send(embed=embed)

    def check(message):
        return (message.author == ctx.author
                and (message.content == "cancel"
                     or string_is_int(message.content)))
    try:
        msg = await bot.wait_for("message", check=check, timeout=15)
        if msg.content == "cancel":
            await ctx.send("Annulé !", delete_after=5)
            await self_message.delete(delay=None)
            await ctx.message.delete(delay=2)
            await msg.delete(delay=1)
        else:
            num = int(msg.content)
            if 0 < num <= len(result):
                url = get_youtube_url(result[num - 1])
                await ctx.send(content=f"{url}")
                await ctx.message.delete(delay=2)
                await self_message.delete(delay=None)
                await msg.delete(delay=1)

    except asyncio.TimeoutError:
        await ctx.send("Tu as pris trop de temps pour répondre !",
                       delete_after=5)
        await self_message.delete(delay=None)
        await ctx.message.delete(delay=2)


@bot.command()
async def comicsblog(ctx, num):
    """Send latest comicsblog news.

    Args:
        num (int): number of results to send

    """
    list = get_comicsblog(num)
    embed = discord.Embed(title=f"les {num} derniers articles de comicsblog",
                          color=0xe3951a)
    for l in list:
        embed.add_field(name=l.find('title').text, value=l.find('guid').text,
                        inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def kick(ctx):
    """Kick user."""
    member_list = ctx.message.mentions
    if ctx.author.top_role >= bot.role_modo:
        for member in member_list:
            await member.kick()
    else:
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501


@bot.command()
async def ban(ctx):
    """Ban user."""
    member_list = ctx.message.mentions
    if ctx.author.top_role >= bot.role_modo:
        for member in member_list:
            await member.ban(delete_message_days=3)
    else:
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501


@bot.command()
async def google(ctx, *, query):
    """Send first Google search result."""
    try:
        result = google_top_link(query)
        await ctx.send(content=f"{result['title']}\n {result['url']}")
    except TypeError:
        pass


@bot.command()
async def googlelist(ctx, num, *, args):
    """Send Google search results."""
    result = search_google(args, num)
    embed = discord.Embed(title=f"Les {num} premiers résultats de la recherche",  # noqa: E501
                          color=0x3b5cbe)
    for r in result:
        embed.add_field(name=r['title'], value=r['url'], inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def timer(ctx, numb, *, args):
    """Program a timer."""
    num = int(numb)
    await ctx.send(content=f"{ctx.author.mention} : timer enregistré !",
                   delete_after=10)
    await asyncio.sleep(num, result=None, loop=None)
    await ctx.send(content=f"temps écoulé ! : {ctx.author.mention} {args}")


@bot.command()
async def roulette(ctx):
    """Plays russian roulette and kick user if shot."""
    if random.randrange(6) == 3:
        await ctx.send(content=f"Pan !")
        await ctx.send(content=snap_url, delete_after=4)
        await asyncio.sleep(2.4, result=None, loop=None)
        await ctx.author.kick()
    else:
        await ctx.send(content="*clic*....Tu restes vivant !")


@bot.command()
async def gif(ctx, name):
    """Send gif corresponding to 'name'."""
    name = name.lower()
    if name == 'help':

        try:  # if in team category
            if ctx.channel.category_id == dcteam_category_id:
                list_names = my_giflist.get_names_string(private=False)
            else:
                list_names = my_giflist.get_names_string(private=True)
        except AttributeError:
            list_names = my_giflist.get_names_string(private=True)
            # channel.category_id will fail in DM messages
            # DMChannel' object has no attribute 'category_id

        embed = discord.Embed(title="liste des gifs",
                              description=list_names, color=0x000FF)
        await ctx.send(embed=embed)

    if my_giflist.get_gif(name) is not None:
        embed = discord.Embed()
        try:
            if (my_giflist.get_gif(name)['public']
                    or ctx.channel.category_id == dcteam_category_id):
                gif_url = my_giflist.get_gif(name)['url']
                embed.set_image(url=gif_url)
                await ctx.send(embed=embed)
        except AttributeError:
            # channel.category_id will fail in DM messages
            # DMChannel' object has no attribute 'category_id
            if my_giflist.get_gif(name)['public']:
                gif_url = my_giflist.get_gif(name)['url']
                embed.set_image(url=gif_url)
                await ctx.send(embed=embed)
    else:
        pass


@bot.command()
async def admin(ctx):
    """Help for admin user."""
    embed = discord.Embed(color=0x0000FF)
    embed.add_field(name="gifadd",
                    value="!gifadd <name> <url> <bool> (bool : public(True) or private(False) )",  # noqa: E501
                    inline=False)
    embed.add_field(name="gifdelete", value="!gifdelete <name>", inline=False)
    if ctx.author.top_role > bot.guild.get_role(admin_id):
        await ctx.author.send(embed=embed)


@bot.command()
async def gifadd(ctx, name, url, bool):
    """Add gif in gif dictionary and gif json file."""
    name = name.lower()
    if ctx.author.top_role > bot.guild.get_role(admin_id):
        my_giflist.gif_add(name, url, bool)
    else:
        pass


@bot.command()
async def gifdelete(ctx, name):
    """Delete gif in gif dictionary and gif json file."""
    name = name.lower()
    if ctx.author.top_role > bot.guild.get_role(admin_id):
        my_giflist.gif_delete(name)
    else:
        pass


@bot.command()
@commands.has_any_role(*admin_role)
async def restart(ctx):
    """Restart bot."""
    await ctx.send('Restarting.')
    os.execv(__file__, sys.argv)


@restart.error
async def restart_error(ctx, error):
    """Handle error in !restart command (MissingAnyRole)."""
    await ctx.send('Nope.')


@bot.command()
async def choose(ctx, *choices):
    """Randomly choose user's choices."""
    if len(choices) < 1:
        return None
    await ctx.send(random.choice(choices))


@bot.command()
async def coinflip(ctx):
    """Launch a coinflip and print 'pile' or 'face'."""
    await ctx.send(random.choice(["pile", "face"]))


@bot.command()
async def say(ctx, *, args):
    """Bot writes user message content, and delete original user message."""
    await ctx.message.delete()
    await ctx.send(content=args)


@bot.command()
async def header(ctx, arg):
    """Send header image."""
    arg = arg.lower()
    monthly = get_monthly_url()
    embed = discord.Embed(title="Comics du mois", url=monthly)
    if arg == "rebirth" or arg == "dcrebirth":
        file_path = get_header(1)
        await ctx.send(embed=embed, file=discord.File(file_path))
        os.remove(file_path)
    elif arg == "hors" or arg == "horsrebirth":
        file_path = get_header(2)
        await ctx.send(embed=embed, file=discord.File(file_path))
        os.remove(file_path)
    elif arg in ["indé", "indés", "inde", "indé"]:
        file_path = get_header(3)
        await ctx.send(embed=embed, file=discord.File(file_path))
        os.remove(file_path)
    elif arg == "marvel":
        file_path = get_header(4)
        await ctx.send(embed=embed, file=discord.File(file_path))
        os.remove(file_path)


@bot.event
async def on_message(ctx):
    """Read all message and check if it's a gif command."""
    found = False
    channel = ctx.channel
    # Find if custom command exist in dictionary
    embed = discord.Embed()
    for key in my_giflist.gifs.keys():
        # Added simple hardcoded prefix
        command = '!' + key
        if ctx.content.lower() == command:
            found = True
            try:
                if (my_giflist.get_gif(key)['public']
                        or ctx.channel.category_id == dcteam_category_id):
                    gif_url = my_giflist.get_gif(key)['url']
                    embed.set_image(url=gif_url)
                    await channel.send(embed=embed)
            except AttributeError:
                # channel.category_id will fail in DM messages
                # DMChannel' object has no attribute 'category_id
                if my_giflist.get_gif(key)['public']:
                    gif_url = my_giflist.get_gif(key)['url']
                    embed.set_image(url=gif_url)
                    await channel.send(embed=embed)
    # If not b
    if not found:
        await bot.process_commands(ctx)

# time=date.time(hour=10)  will use it when v1.3 for discord.py is released
@tasks.loop(hours=24)  # will take time as argument when v1.3 is released  # noqa: E501
async def bonjour_madame():
    """Send daily bonjourmadame."""
    if 0 <= datetime.date.today().weekday() <= 5:  # check the current day, days are given as numbers where Monday=0 and Sunday=6
        embed = discord.Embed()
        embed.set_image(url=latest_madame())
        embed.set_footer(text="Bonjour Madame")
        await bot.get_channel(nsfw_channel_id).send(embed=embed)


@bonjour_madame.before_loop
async def before_bonjour_madame():
    # TODO : doctring
    await bot.wait_until_ready()


@bot.command()
async def nsfw(ctx):
    # TODO : doctring
    if ctx.channel.id == nsfw_channel_id:
        await ctx.send(content=reddit_nsfw())

@bot.command()
async def poke(ctx, people):
    """Send card made by Slyrax """
    people = people.lower()
    if people == "help" : #probably needs improvements
        embed=discord.Embed(title="Liste des cartes \nSyntaxe : !poke <nom>",description=poke_help) #use this to get by until improvement
        embed.set_footer(text="Merci à Slyrax pour les cartes !")
        await ctx.send(embed=embed)

    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        card_file = os.path.join(dir_path, f"pictures/cards/{people}.jpg")
        f = discord.File(fp=card_file, filename=people+".jpg") #discord.File can't handle f-strings apparently
        embed = discord.Embed()
        embed.set_image(url="attachment://"+people+".jpg") #better safe than sorry
        await ctx.send(file=f, embed=embed)
bonjour_madame.start()
bot.run(token)
