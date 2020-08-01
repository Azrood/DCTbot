#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Register cog."""

import asyncio
from secrets import token_hex
import time
from discord.ext import commands
from pyphpbb_sl import PhpBB

from utils.secret import forum_host, forum_user_name, forum_password


async def try_to_verify(other_member, token):
    """Fetch unread messages and try to read PM from 'other_member'.

    Compare PM content to token.
    """
    # Connect to phpbb forum and fetch unread PM
    async with PhpBB(forum_host) as phpbb:
        await phpbb.login(forum_user_name, forum_password)
        await phpbb.fetch_unread_messages()
        # Read message from expected user
        message_to_read = phpbb.find_expected_message_by_user(other_member)
        if message_to_read:
            message = await phpbb.read_private_message(message_to_read)
            if message['content'] == token:
                print("Valid token ! GOOD")
                return True
            else:
                print("Invalid token ! BAD !")
                return False
        return False


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        """Register User."""
        content = ("Salut !\n\nNous allons essayer de valider ta demande pour "
                   "te lier à ton compte sur le forum.\n\n"
                   "Pour valider ta demande, réponds moi avec ton "
                   "pseudonyme (= identifiant pour le Forum), STP.\n")
        await ctx.author.send(content)

        dmchannel = ctx.author.dm_channel

        def check(m):
            return m.author == ctx.author and m.channel == dmchannel

        msg = await self.bot.wait_for('message', check=check)

        user_to_validate = msg.content

        await dmchannel.send("Ok, nous allons procéder pour vérifier que "
                             "tu es bien le propriétaire du compte forum "
                             "suivant :\n"
                             f"\t{user_to_validate}")

        token = token_hex(16)
        await dmchannel.send("J'ai besoin que tu m'envoies le token suivant, "
                             "sur le FORUM.\n"
                             "Envoie un 'Message Privé' (sur le __forum__ à) :\n"
                             "\tDC-Trad\n"
                             "contenant le token suivant : \n"
                             f"\t{token}\n"
                             "(ce token expire dans 5 minutes).")

        timeout = time.time() + 5 * 60   # 5 minutes from now
        while True:
            await asyncio.sleep(30)  # will fetch PM every 30 seconds
            if time.time() > timeout:
                break
            valid = await try_to_verify(user_to_validate, token)
            if valid:
                await dmchannel.send("YATTA ! tu as envoyé le bon token.\n"
                                     "(mais le code pour t'enregistrer dans "
                                     "une database n'est pas codé.)")
                return True

        await dmchannel.send("Malheureusement, je n'ai pas pu vérifier ton compte.")
