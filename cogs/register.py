#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Register cog."""

import logging
from secrets import token_hex
from discord.ext import commands
from pyphpbb_sl import PhpBB

from utils.secret import forum_host, forum_user_name, forum_password

logger = logging.getLogger(__name__)


async def send_token(forum_member, discord_member, token):
    """send token via forum MP."""
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

        msg = await self.bot.wait_for('message', check=check, timeout=60)

        user_to_validate = msg.content

        logger.info("%20s tries to register with forum name  %20s", ctx.author, user_to_validate)  # noqa: E501

        await dmchannel.send("Ok, nous allons procéder pour vérifier que "
                             "tu es bien le propriétaire du compte forum "
                             "suivant :\n"
                             f"\t{user_to_validate}")

        token = token_hex(16)

        async with dmchannel.typing():
            pm_is_sent = await send_token(user_to_validate, ctx.author, token)

        if pm_is_sent:
            await dmchannel.send("Je t'ai envoyé un Message Privé sur le Forum,\n"
                                 "contenant un 'token'. Va lire tes MP sur le "
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
            return

        msg2 = await self.bot.wait_for('message', check=check, timeout=300)

        if token in msg2.content:
            await dmchannel.send("YATTA ! tu as envoyé le bon token.\n"
                                 "(mais le code pour t'enregistrer dans "
                                 "une database n'est pas codé.)")
            # TODO : do stuff here to save
            logger.info("%20s successfully verified his forum account %15s", ctx.author, user_to_validate)  # noqa: E501
            return True

        await dmchannel.send("Malheureusement, je n'ai pas pu vérifier ton "
                             "compte.\nPour recommencer, réessayer la "
                             "commande register dans un salon.")
        logger.warning("%20s FAILS to verified his forum account %19s", ctx.author, user_to_validate)  # noqa: E501
        return False
