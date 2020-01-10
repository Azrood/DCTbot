"""Cog to send notifications (on video games, etc...)."""

import discord
from discord.ext import commands

from utils.secret import react_role_msg_id


freegame_on = "Vous serez notifié lorsqu'un jeu gratuit sera posté !"
freegame_off = "Vous __**ne**__ serez __**plus**__ notifié lorsqu'un jeu gratuit sera posté !"  # noqa:E501
newrelease_on = "Vous serez notifié lorsqu'une release sera postée !"
newrelease_off = "Vous __**ne**__ serez __**plus**__ notifié lorsqu'une release sera postée!"  # noqa:E501


class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Read all the reactions added (even those not in cache)
            and filter by messageID to check the message where the reaction
            was removed and give the user whose reaction was removed
            a specific role
        """
        user = self.bot.guild.get_member(payload.user_id)

        # video_game emoji -> free games notification subscribe
        if (payload.emoji.name == "\U0001f3ae"
                and payload.message_id == react_role_msg_id):
            freegame_role = discord.utils.get(self.bot.guild.roles,
                                              name="jeux gratuits")
            await user.add_roles(freegame_role)
            await user.send(content=freegame_on)

        # ring_bell emoji -> new releases notification subscribe
        if (payload.emoji.name == "\U0001f514"
                and payload.message_id == react_role_msg_id):
            header_role = discord.utils.get(self.bot.guild.roles,
                                            name="header release")
            await user.add_roles(header_role)
            await user.send(content=newrelease_on)

        # leave team but stay friend
        if (payload.emoji.name == "\U0000274C"
                and payload.message_id == 654272251276820501):
            roles = user.roles[1:]
            keupains_role = discord.utils.get(self.bot.guild.roles,
                                              name="Keupains")
            await user.remove_roles(*roles)
            await user.add_roles(keupains_role)
            await user.send(content="Keupains pour toujours et à jamais !")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Read all the reactions removed (even those not in cache)
            and filter by messageID to check the message where the reaction
            was removed and give the user whose reaction was removed
            a specific role
        """
        user = self.bot.guild.get_member(payload.user_id)

        # video_game emoji -> free games notification unsubscribe
        if (payload.emoji.name == "\U0001f3ae"
                and payload.message_id == react_role_msg_id):
            freegame_role = discord.utils.get(self.bot.guild.roles,
                                              name="jeux gratuits")
            await user.remove_roles(freegame_role)
            await user.send(content=freegame_off)

        # ring_bell emoji -> new releases notification unsubscribe
        if (payload.emoji.name == "\U0001f514"
                and payload.message_id == react_role_msg_id):
            header_role = discord.utils.get(self.bot.guild.roles,
                                            name="header release")
            await user.remove_roles(header_role)
            await user.send(content=newrelease_off)
