#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import asyncio
import datetime
import os
import sys
import time

import discord
from discord.ext import commands, tasks

from cogs.getcomics import Getcomics
from cogs.google import Google
from cogs.misc import Misc
from cogs.urban import Urban

from utils.bonjourmadame import latest_madame
from utils.comicsblog import get_comicsblog
from utils.gif_json import GifJson
from utils.header import get_header, get_monthly_url
from utils.logs import CommandLog
from utils.reddit import reddit_nsfw
from utils.secret import (token, dcteam_role_id, dcteam_id, modo_role_id,
                          dcteam_category_id, nsfw_channel_id,
                          admin_role, staff_role, mods_role, react_role_msg_id)
from utils.tools import string_is_int, args_separator_for_log_function
from utils.youtube import youtube_top_link, search_youtube, get_youtube_url

prefix = '!'

if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        print("You are in debug mode.")
        print("Prefix is now '?'")
        prefix = '?'

bot = commands.Bot(command_prefix=prefix, help_command=None,
                   description=None, case_insensitive=True)


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
    {'name': 'choose', 'value': "choisit aléatoiremement parmi plusieurs arguments \n Syntaxe : !choose arg1 arg2 \"phrase avec plusieurs mots\" (si vous voulez des choix avec plusieurs mots, mettez vos choix entre \"\" comme par exemple \n !choose \"manger chinois\" \"manger italien \" \" manger quelqu'un \" ) "},  # noqa: E501
    {"name": "coinflip", 'value': "fais un lancer de pile ou face"},
    {'name': 'say', 'value': "répète ce qui est entré et supprime le message du user"},  # noqa: E501
    {'name': 'ping', 'value': "Ping le bot pour voir s'il est en ligne"}
    ]
help_team = [
    {'name': 'team', 'value': 'assigne le rôle DCTeam au(x) membre(s) mentionné(s)'},  # noqa: E501
    {'name': 'clear', 'value': 'efface le nombre de message entré en argument (!clear [nombre])'}  # noqa: E501
    ]
help_above = [
    {'name': 'kick', 'value': 'kick la(les) personne(s) mentionnée(s)\n (syntaxe : !kick [@membre] (optionel)[@membre2]...'},  # noqa: E501
    {'name': 'ban', 'value': 'bannit le(s) user(s) mentionné(s)\n Syntaxe : !ban [@membre1][@membre2]....'},  # noqa: E501
    {'name': 'nomorespoil', 'value': 'spam des "..." pour cacher les spoils'}
    ]

poke_help = "azrod\nbane\nrun\nsergei\nxanatos\nphoe"  # see comment in line 509

dir_path = os.path.dirname(os.path.realpath(__file__))
my_giflist = GifJson("gifs.json")
log = CommandLog("logs.json")

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
    channel_general = discord.utils.get(bot.guild.text_channels, name='general')
    greeting = random.choice(["Bonjour tout le monde !",
                            "Yo tout le monde ! Vous allez bien ?",
                            "Comment allez-vous en cette magnifique journée ?",
                            "Yo les biatches !",
                            "Good morning motherfuckers !",
                            "Yo les gros ! ça roule ?",
                            "Yo les juifs ! ça gaze ?",
                            "Hola amigos ! Bonne journée !",
                            "Roulette pour tout le monde ! TOUT DE SUITE !!",
                            "I'm back bitches !",
                            "Ohayo gozaimasu !",
                            "Je suis de retour pour vous jouer un mauvais tour !",
                            "Wake up ! Grab a brush and put a little makeup !",
                            "Wake me up ! Wake me up inside !"
                            ]
                        )
    await asyncio.sleep(delay=36000) # bot is rebooted every day at 00:00 so we wait 10 hours after logging in
    await channel_general.send(content=greeting)


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
    # if ctx.channel.category_id == dcteam_category_id:
        # embed.add_field(name='nsfw', value="affiche une image nsfw", inline=False)  # noqa: E501
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
@commands.has_any_role(*staff_role)
async def team(ctx):
    """Give 'team' role to user list."""
    member_list = ctx.message.mentions  # une liste d'objets
    counter = 0
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


@team.error
async def team_error(ctx, error):
    """Handle error in command !team (MissingAnyRole)."""
    await ctx.send(content="Bien tenté mais tu n'as pas de pouvoir ici !")


@bot.command()
@commands.has_any_role(*staff_role)
async def clear(ctx, number):
    """Clear n messages."""
    nbr_msg = int(number)
    messages = await ctx.channel.history(limit=nbr_msg + 1).flatten()
    await ctx.channel.delete_messages(messages)
    await ctx.send(content=f"J'ai supprimé {nbr_msg} messages", delete_after=5)
    today = datetime.date.today().strftime("%d/%m/%Y")
    time = datetime.datetime.now().strftime("%Hh%Mm%Ss")
    log.log_write(today, time,
                  ctx.channel.name.lower(),
                  ctx.command.name.lower(),
                  ctx.author.name.lower())


@clear.error
async def clear_error(ctx, error):
    """Handle error in !clear command (MissingAnyRole)."""
    await ctx.send(content=f"Tu n'as pas le pouvoir{ctx.author.mention} !")


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
    list = await get_comicsblog(num)
    embed = discord.Embed(title=f"les {num} derniers articles de comicsblog",
                          color=0xe3951a)
    for l in list:
        embed.add_field(name=l.find('title').text, value=l.find('guid').text,
                        inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_any_role(*mods_role)
async def kick(ctx):
    """Kick user."""
    member_list = ctx.message.mentions
    for member in member_list:
        await member.kick()
    today = datetime.date.today().strftime("%d/%m/%Y")
    time = datetime.datetime.now().strftime("%Hh%Mm%Ss")
    log.log_write(today, time,
                  ctx.channel.name.lower(),
                  ctx.command.name.lower(),
                  ctx.author.name.lower())
    await ctx.send(content="Adios muchachos !")


@kick.error
async def kick_error(ctx, error):
    """Handle error in !kick command (MissingAnyRole)."""
    await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501


@bot.command()
@commands.has_any_role(*mods_role)
async def ban(ctx):
    """Ban user."""
    member_list = ctx.message.mentions
    for member in member_list:
        await member.ban(delete_message_days=3)
    today = datetime.date.today().strftime("%d/%m/%Y")
    time = datetime.datetime.now().strftime("%Hh%Mm%Ss")
    log.log_write(today, time,
                  ctx.channel.name.lower(),
                  ctx.command.name.lower(),
                  ctx.author.name.lower())


@ban.error
async def ban_error(ctx, error):
    """Handle error in !ban command (MissingAnyRole)."""
    await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501


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
@commands.is_owner()
async def admin(ctx):
    """Help for admin user."""
    embed = discord.Embed(color=0x0000FF)
    embed.add_field(name="gifadd",
                    value="!gifadd <name> <url> <bool> (bool : public(True) or private(False) )",  # noqa: E501
                    inline=False)
    embed.add_field(name="gifdelete", value="!gifdelete <name>", inline=False)
    embed.add_field(name="log_latest", value="!log_latest <int>", inline=False)
    embed.add_field(name="logs", value="!logs <date> <user> <command> <channel>\n args are optional for filtering, for today, say <date> = today. Otherwise date=dd/mm/yyyy", inline=False)  # noqa:E501
    embed.add_field(name="sleep", value="make the bot sleep for <numb> seconds\n  Syntax : !sleep <number>", inline=False)
    embed.add_field(name="kill", value="Kill the bot.", inline=False)
    await ctx.author.send(embed=embed)


@bot.command()
@commands.is_owner()
async def gifadd(ctx, name, url, bool):
    """Add gif in gif dictionary and gif json file."""
    name = name.lower()

    bool = bool.lower()
    my_giflist.gif_add(name, url, bool)
    await ctx.send(content=f"gif {name} ajouté !", delete_after=2)


@bot.command()
@commands.is_owner()
async def gifdelete(ctx, name):
    """Delete gif in gif dictionary and gif json file."""
    name = name.lower()
    my_giflist.gif_delete(name)
    await ctx.send(content=f"gif {name} supprimé !", delete_after=2)


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
async def header(ctx, arg):
    """Send header image."""
    arg = arg.lower()
    monthly = await get_monthly_url()
    embed = discord.Embed(title="Comics du mois", url=monthly)
    if arg == "rebirth" or arg == "dcrebirth":
        file_path = await get_header(1)
        await ctx.send(embed=embed, file=discord.File(file_path))
        os.remove(file_path)
    elif arg == "hors" or arg == "horsrebirth":
        file_path = await get_header(2)
        await ctx.send(embed=embed, file=discord.File(file_path))
        os.remove(file_path)
    elif arg in ["indé", "indés", "inde", "indé"]:
        file_path = await get_header(3)
        await ctx.send(embed=embed, file=discord.File(file_path))
        os.remove(file_path)
    elif arg == "marvel":
        file_path = await get_header(4)
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
        command = prefix + key
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
    if 0 <= datetime.date.today().weekday() <= 4:  # check the current day, days are given as numbers where Monday=0 and Sunday=6  # noqa: E501
        embed = discord.Embed()
        embed.set_image(url=await latest_madame())
        embed.set_footer(text="Bonjour Madame")
        await bot.get_channel(nsfw_channel_id).send(embed=embed)


@bonjour_madame.before_loop
async def before_bonjour_madame():
    """Intiliaze bonjour_madame loop."""
    await bot.wait_until_ready()
    await asyncio.sleep(37800)  # Wait 10hours 30min, to lauch at 10:30AM


# @bot.command()
# @commands.is_nsfw()
# async def nsfw(ctx):
    # TODO : doctring
    # await ctx.send(content=reddit_nsfw())

@bot.command()
async def poke(ctx, people):
    """Send card made by Slyrax."""
    people = people.lower()
    if people == "help":  # probably needs improvements
        embed = discord.Embed(title="Liste des cartes \nSyntaxe : !poke <nom>", description=poke_help)  # use this to get by until improvement  # noqa: E501
        embed.set_footer(text="Merci à Slyrax pour les cartes !")
        await ctx.send(embed=embed)

    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        card_file = os.path.join(dir_path, f"pictures/cards/{people}.jpg")
        f = discord.File(fp=card_file, filename=people+".jpg")  # discord.File can't handle f-strings apparently  # noqa: E501,E226
        embed = discord.Embed()
        embed.set_image(url="attachment://"+people+".jpg")  # better safe than sorry  # noqa: E501,E226
        await ctx.send(file=f, embed=embed)


@bot.command()
@commands.is_owner()
async def logs(ctx, date, *args):
    """Send some logs in private message about moderation commands usage.

    Args:
        date (str): today or date as DD/MM/YYYY
        args: up to 3 elements, speifying command, user, channel

    Examples:
        log today homer general: list homer commands in #general channel
        log 05/06/2019 faq: list all moderaiton commands in #faq on 05/06/2019

    """
    embed = discord.Embed(title="logs", colour=0xe7191f)

    # arg_lists is always ["user", "command", "channel"]
    args_list = args_separator_for_log_function(bot.guild, args)

    if date == "today":
        date = datetime.date.today().strftime("%d/%m/%Y")

    bin_array = [int(i is not None) for i in args_list]  # convert ["foo", None, None] to [1, 0, 0]  # noqa:E501
    n = int("".join(str(x) for x in bin_array), 2)  # binary array to int

    user, command, channel = args_list

    if log.log_read(date, *args_list) is not None:  # if it is None, there are no logs on the given date  # noqa:E501

        # we get a list of tuple in this format [(time,user,command,channel)]
        list_log = log.log_read(date, *args_list)  # to avoid multiple calling

        # if entries are not specified, then they are None
        if n == 0:  # [None, None, None]
            for v in list_log:
                embed.add_field(name=v[0], value=f"{v[1]} used {v[2]} in {v[3]}", inline=False)  # nice embed  # noqa:E501

        elif n == 1:  # [None, None, channel]
            embed.set_footer(text=channel)
            for v in list_log:
                embed.add_field(name=v[0], value=f"{v[1]} used {v[2]}", inline=False)  # noqa:E501

        elif n == 2:  # [None, command, None]
            embed.set_footer(text=f"users of {command}")
            for v in list_log:
                embed.add_field(name=v[0], value=f"{v[1]} in {v[2]}", inline=False)  # noqa:E501

        elif n == 3:  # [None, command, channel]
            embed.set_footer(text=f"users of {command} in {channel}")
            for v in list_log:
                embed.add_field(name=v[0], value=f"{v[1]}", inline=False)

        elif n == 4:  # [user, None, None]
            embed.set_footer(text=user)
            for v in list_log:
                embed.add_field(name=v[0], value=f"used {v[1]} in {v[2]}", inline=False)  # noqa:E501

        elif n == 5:  # [user, None, channel]
            embed.set_footer(text=f"{user} commands in {channel}")
            for v in list_log:
                embed.add_field(name=v[0], value=f"used {v[2]}", inline=False)

        elif n == 6:  # [user, command, None]
            embed.set_footer(text=f"{user} used {command}")
            for v in list_log:
                embed.add_field(name=v[0], value=f"used in {v[2]}", inline=False)  # noqa:E501

        else:  # [user, command, channel]
            embed.set_footer(text=f"{user} used {command} in {channel}")
            for v in list_log:
                embed.add_field(name=v[0], value=f"{v[1]}", inline=False)

        await ctx.author.send(embed=embed)
    else:  # no logs in the given date
        await ctx.author.send(content="Rien dans cette date !")


@bot.command()
@commands.is_owner()
async def log_latest(ctx, numb=10):
    """Send latest logs."""
    embed = discord.Embed(title="latest logs")
    latest = log.log_latest(int(numb))
    for i in latest:
        embed.add_field(name='\u200B', value=i, inline=False)
    await ctx.author.send(embed=embed)


@bot.command()
@commands.has_any_role(*mods_role)
async def nomorespoil(ctx):
    """Spam dots to clear potential spoils."""
    await ctx.send("\n".join(["..." for i in range(50)]))

@bot.command()
@commands.is_owner()
async def sleep(ctx,numb):
    """`time` is blocking for async functions. Delay the bots for `numb` seconds"""
    await ctx.send(content=f"Going to sleep for {numb} seconds. Good night !")
    time.sleep(int(numb))
    morning = random.choice(["Good morning !",
                            "Bonjour !"
                            ]
                        )
    await ctx.send(content=morning)

@bot.command()
@commands.is_owner()
async def kill(ctx):
    """Kill the bot."""
    await bot.logout()


@bot.event
async def on_raw_reaction_add(payload):
    """Read all the reactions added (even those not in cache) 
        and filter by messageID to check the message where the reaction was removed
        and give the user whose reaction was removed a specific role
    """
    user = bot.guild.get_member(payload.user_id)
    if payload.emoji.name == "\U0001f3ae" and payload.message_id == react_role_msg_id:
        freegame_role = discord.utils.get(bot.guild.roles, name="jeux gratuits")
        await user.add_roles(freegame_role)
        await user.send(content="Vous serez notifié lorsqu'un jeu gratuit sera posté !")
    if payload.emoji.name == "\U0001f514" and payload.message_id == react_role_msg_id:
        header_role = discord.utils.get(bot.guild.roles, name="header release")
        await user.add_roles(header_role)
        await user.send(content="Vous serez notifié lorsqu'une release sera postée !")

@bot.event
async def on_raw_reaction_remove(payload):
    """Read all the reactions removed (even those not in cache) 
        and filter by messageID to check the message where the reaction was removed
        and give the user whose reaction was removed a specific role
    """
    user = bot.guild.get_member(payload.user_id)
    if payload.emoji.name == "\U0001f3ae" and payload.message_id == react_role_msg_id:
        freegame_role = discord.utils.get(bot.guild.roles, name="jeux gratuits")
        await user.remove_roles(freegame_role)
        await user.send(content="Vous __**ne**__ serez __**plus**__ notifié lorsqu'un jeu gratuit sera posté !")
    if payload.emoji.name == "\U0001f514" and payload.message_id == react_role_msg_id:
        header_role = discord.utils.get(bot.guild.roles, name="header release")
        await user.remove_roles(header_role)
        await user.send(content="Vous __**ne**__ serez __**plus**__ notifié lorsqu'une release sera postée!")


bonjour_madame.start()

bot.add_cog(Getcomics(bot))
bot.add_cog(Google(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Urban(bot))

bot.run(token)
