#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import asyncio
import datetime
import os
import sys
import random

import discord
from discord.ext import commands, tasks

from cogs.comicsblog import Comicsblog
from cogs.getcomics import Getcomics
from cogs.google import Google
from cogs.header import Header
from cogs.misc import Misc
from cogs.urban import Urban
from cogs.team import Team
from cogs.mod import Mod
from cogs.admin import Admin
from cogs.youtube import Youtube

from utils.logs import CommandLog
from utils.bonjourmadame import latest_madame
from utils.gif_json import GifJson
from utils.reddit import reddit_nsfw
from utils.secret import (token, dcteam_role_id, dcteam_id, modo_role_id,
                          dcteam_category_id, nsfw_channel_id, react_role_msg_id
                          )

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

my_giflist = GifJson("gifs.json")

cogs = [Comicsblog, Getcomics, Google, Header, Urban, Team, Misc, Mod, Youtube, Admin]


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
    bot.log = CommandLog("logs.json")
    bot.gifs = GifJson("gifs.json")
    for cog in cogs:
        bot.add_cog(cog(bot))
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

                        
bot.run(token)
