#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Register cog."""

from collections import namedtuple
import json
import logging
from pathlib import Path
from secrets import token_hex
from typing import Union

import discord
from discord.ext import commands
from pyphpbb_sl import PhpBB
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

from utils.secret import forum_host, forum_user_name, forum_password, mods_role

logger = logging.getLogger(__name__)

Role = namedtuple('Role', ['id'])

DB_FILE = "register.db"
DB_PATH = Path(__file__).resolve().parent / DB_FILE


def quote_id(id):
    """Add quotes around intger

    Args:
        id (int): an ID

    Returns:
        str: ID with quotes

    Example:
        >>> quote_id(35483543)
        '"35483543"'

    """
    return '"' + str(id) + '"'


async def send_token(forum_member, discord_member, token):
    """Send token via forum MP

    Args:
        forum_member (str): Username (forum) to send token to
        discord_member (discord.Member): discord Member who requested token
        token (str): token to send

    Returns:
        bool: success for sending the Private Message

    """
    subject = "Token de validation pour le Discord"
    message = ("Voici le token que vous avez demandé sur Discord "
               f"(utilisateur {discord_member}) :\n\n"
               f"\t{token}\n\n"
               "si vous n'êtes pas à l'origine de cette demande "
               "merci d'ignorer ce message")

    async with PhpBB(forum_host) as phpbb:
        await phpbb.login(forum_user_name, forum_password)
        success = await phpbb.send_private_message(receiver=forum_member,
                                                   subject=subject,
                                                   message=message)
    return success


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database(DB_PATH)

    async def save_in_db(self, ctx, discord_member, username):
        """Record user in database."""
        async with PhpBB(forum_host) as phpbb:
            await phpbb.login(forum_user_name, forum_password)
            uid, rank = await phpbb.get_member_infos(username)
        logger.info("Forum account %20s (%8d) with rank %15s for member %10s successfully verified (asked by %10s)", username, uid, rank, discord_member, ctx.author)  # noqa: E501

        # table names are guild IDS, with double quotes (sqlite thing, digits alone wont work)
        table = self.db.table(quote_id(ctx.guild.id))
        table.upsert({"discord_id": discord_member.id, "forum_id": uid,
                      "discord_name": discord_member.display_name, "forum_name": username,
                      "discord_roles": [role.id for role in discord_member.roles if role.name != "@everyone"],
                      "forum_rank": rank
                      },
                     pk="discord_id")
        logger.info("database has been updated")

    @commands.command()
    async def register(self, ctx):
        """Allow someone to register itself in the database.

        Phase 1: the bot send instructions (discord private message)
        Phase 2: the bot expects a 'Username' (for forum) in discord PM response
        Phase 3: the bot send a token to the forum user (forum PM)
        Phase 4: bot expects the token in discord PM, and compare.
            if token match, user is saved in the database

        """
        # Phase 1 : send instructions #########################################
        content = ("Salut !\n\nNous allons essayer de valider ta demande pour "
                   "te lier à ton compte sur le forum.\n\n"
                   "Pour valider ta demande, réponds moi avec ton "
                   "pseudonyme (= identifiant pour le Forum), STP.\n")
        await ctx.author.send(content)

        # Phase 2 : receiving user name to validate ###########################
        dmchannel = ctx.author.dm_channel

        def check(m):
            return m.author == ctx.author and m.channel == dmchannel

        msg = await self.bot.wait_for('message', check=check, timeout=60)

        user_to_validate = msg.content

        logger.info("%20s tries to register with forum name  %20s", ctx.author, user_to_validate)  # noqa: E501

        # Phase 3 : sending token #############################################
        await dmchannel.send("Ok, nous allons procéder pour vérifier que "
                             "tu es bien le propriétaire du compte forum "
                             "suivant :\n"
                             f"\t{user_to_validate}")

        token = token_hex(16)

        async with dmchannel.typing():
            pm_is_sent = await send_token(user_to_validate, ctx.author, token)

        if pm_is_sent:
            await dmchannel.send("Je t'ai envoyé un Message Privé sur le Forum,"
                                 "contenant un 'token'.\nVa lire tes MP sur le "
                                 "forum, et copie ce token\n\n"
                                 "Ensuite, colle le __ICI__ dans notre "
                                 "conversation Discord et envoie le moi "
                                 "pour que je le vérifie.\n\n"
                                 "(ce token expire dans 5 minutes).")
        else:
            await dmchannel.send("Problème lors de l'envoi du MP forum.\n"
                                 "Probablement dû à une erreur dans le "
                                 "pseudonyme.\n"
                                 "Arrêt de la procédure de validation."
                                 "Pour recommencer, réessayer la commande "
                                 "register.")
            logger.warning("Can't send a Forum PM to %20s, asked by %15s", user_to_validate, ctx.author)  # noqa: E501
            return False

        # Phase 4 : receiving and checking token ##############################
        msg2 = await self.bot.wait_for('message', check=check, timeout=300)

        if token in msg2.content:
            await dmchannel.send("YATTA ! tu as envoyé le bon token.\n"
                                 "Tes rôles ont été enregistrés dans la base de donnée.")

            await self.save_in_db(ctx, ctx.author, user_to_validate)
        else:
            await dmchannel.send("Malheureusement, je n'ai pas pu vérifier ton "
                                 "compte.\nPour recommencer, réessayer la "
                                 "commande register.")
            logger.warning("%20s FAILS to verified his forum account %19s", ctx.author, user_to_validate)  # noqa: E501

    @commands.group()
    async def database(self, ctx):
        """Group for !database commands

        Discord usage:
            !database add @Foobar foobar
            !database read @Foobar
            !database delete @Foobar
            !database dump

        """
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid database command passed...\n'
                           'subcommands are add, delete, read, dump')

    @database.command()
    @commands.has_any_role(*mods_role)
    async def add(self, ctx, member: Union[discord.Member, discord.User], forum_name: str):
        """Add user infos.

        The use of discord.member converter allows to use @mention or id.

        Examples :
            !database add @Foobar foobar
            !database add 320XXXXXXXXXXXX288 foobar

        """
        try:
            await self.save_in_db(ctx, member, forum_name)
            await ctx.send("Done")
        except Exception as e:
            logger.error(e)

    @database.command()
    @commands.has_any_role(*mods_role)
    async def read(self, ctx, member: Union[discord.Member, discord.User]):
        """Read user infos.

        The use of discord.member converter allows to use @mention or id.

        Examples :
            !database read @Foobar
            !database read 320XXXXXXXXXXXX288

        """

        try:
            res = self.db.table(quote_id(ctx.guild.id)).get(int(member.id))
            await ctx.send(res)
        except NotFoundError:
            await ctx.send("user id not found")
        except Exception as e:
            logger.error(e)

    @database.command()
    @commands.has_any_role(*mods_role)
    async def delete(self, ctx, member: Union[discord.Member, discord.User]):
        """Delete user from database.

        The use of discord.member converter allows to use @mention or id.

        Examples :
            !database delete @Foobar
            !database delete 320XXXXXXXXXXXX288

        """
        try:
            self.db.table(quote_id(ctx.guild.id)).delete(int(member.id))
            await ctx.send("Done deleted user from db")
        except NotFoundError:
            await ctx.send("user id not found")
        except Exception as e:
            logger.error(e)

    @database.command()
    @commands.has_any_role(*mods_role)
    async def dump(self, ctx):
        """Send database in an embed (json style).

        Example:
            !database dump

        """
        rows = [json.dumps(r) for r in self.db.table(quote_id(ctx.guild.id)).rows]
        embed = discord.Embed(title="Base de donnée pour cette guilde",
                              description='\n'.join(rows))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        dmchannel = member.dm_channel
        table_name = quote_id(member.guild.id)
        try:
            row = self.db.table(table_name).get(int(member.id))
            role_id_list = json.loads(row.get('discord_roles'))
            role_list = [Role(id=i) for i in role_id_list]
            await member.add_roles(*role_list)
            await dmchannel.send("Tes rôles t'ont été rendus.")
        except NotFoundError:
            pass

    async def cog_command_error(self, ctx, error):
        logger.error(error)
        await ctx.send(error)
