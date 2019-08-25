import discord
import asyncio
import random
from discord.ext import commands, tasks
from utils.secret import token, dcteam_role_id, dcteam_id, modo_role_id, dcteam_category_id, admin_id
from utils.tools import get_command_input, string_is_int
# from utils.urban import get_top_def
from utils.urban import Urban_search
from utils.getcomics import getcomics_top_link
from utils.youtube import youtube_top_link, search_youtube, get_youtube_url
from utils.comicsblog import get_comicsblog
from utils.google import search_google, google_top_link
from utils.gif_json import Gif_json

bot = commands.Bot(command_prefix='!', help_command=None, description=None)

urban_logo = "https://images-ext-2.discordapp.net/external/HMmIAukJm0YaGc2BKYGx5MuDJw8LUbwqZM9BW9oey5I/https/i.imgur.com/VFXr0ID.jpg"

dctradlogo = "http://www.dctrad.fr/ext/planetstyles/flightdeck/store/logodctweb.png"

dctrad_recru = "http://www.dctrad.fr/viewforum.php?f=21"

snap_url = "https://media.tenor.com/images/8d7d2e757f934793bb4154cede8a4afa/tenor.gif"

helps = [
    {'name': 'help', 'value': 'affiche la liste des commandes'},
    {'name': 'gif help', 'value': 'affiche la liste des gifs'},
    {'name': 'getcomics', 'value': 'recherche dans getcomics les mots-clés entrés'},
    {'name': 'urban', 'value': 'fait une recherche du mot entré sur Urban Dictionary'},
    {'name': 'recrutement', 'value': 'donne le lien des tests de DCTrad'},
    {'name': 'timer', 'value': 'minuteur qui notifie le user après X secondes\n Syntaxe : !timer [nombre (secondes)] [rappel]\n Exemple: !timer 3600 organiser mes dossiers'},
    {'name': 'youtube', 'value': 'donne le lien du premier résultat de la recherche'},
    {'name': 'youtubelist', 'value': 'donne une liste de liens cliquables.\n Syntaxe : !youtubelist [nombre] [recherche]'},
    {'name': 'comicsblog', 'value': 'donne les X derniers articles de comicsblog\n (syntaxe : !comicsblog [numero])'},
    {'name': 'google', 'value': 'donne le premier lien de la recherche google avec les mots-clés saisis'},
    {'name': 'googlelist', 'value': 'donne une liste des X premiers liens de la recherche google\n Syntaxe : !googlelist [numero] [mots-clés] \nExemple : !googlelist 3 the final countdown'},
    {'name': 'roulette', 'value': '1/6 chance de se faire kick, la roulette russe avec le bon Colt !'},
    {'name': 'choose', 'value': "choisit aléatoiremement parmi plusieurs arguments \n Syntaxe : !choose arg1 arg2 \"phrase avec plusieurs mots\" (si vous voulez des choix avec plusieurs mots, mettez vos choix entre \"\" comme pâr exemple \n !choose \"manger chinois\" \"manger italien \" \" manger quelqu'un \" ) "},
    {"name": "coinflip", 'value': "fais un lancer de pile ou face"},
    {'name': 'say', 'value': "répète ce qui est entré et supprime le message du user"}
    ]
help_team = [
    {'name': 'team', 'value': 'assigne le rôle DCTeam au(x) membre(s) mentionné(s)'},
    {'name': 'clear', 'value': 'efface le nombre de message entré en argument (!clear [nombre])'}
    ]
help_above = [
    {'name': 'kick', 'value': 'kick la(les) personne(s) mentionnée(s)\n (syntaxe : !kick [@membre] (optionel)[@membre2]...'},
    {'name': 'ban', 'value': 'bannit le(s) user(s) mentionné(s)\n Syntaxe : !ban [@membre1][@membre2]....'}
    ]

my_giflist = Gif_json("utils/gifs.json")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.guild = bot.get_guild(dcteam_id)  # se lier au serveur à partir de l'ID
    bot.role_dcteam = bot.guild.get_role(dcteam_role_id)
    bot.role_modo = bot.guild.get_role(modo_role_id)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Page 1/2, utilisez les flèches en réaction pour naviguer", description="Liste des commandes(toutes les commandes doivent être précédées du prefix \"!\") :", color=0x0000FF)
    embed_2 = discord.Embed(title="Page 2/2, utilisez les flèches en réaction pour naviguer", description="Liste des commandes(toutes les commandes doivent être précédées du prefix \"!\") :", color=0x0000FF)
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
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("\U000025c0")
    await msg.add_reaction("\U000025b6")

    @tasks.loop(seconds=2)
    async def helperloop():
        def check(reaction, user):
            return ctx.author == user and str(reaction.emoji) in ["\U000025b6", "\U000025c0"] and msg.id == reaction.message.id
        reaction, user = await bot.wait_for("reaction_add", check=check, timeout=60)
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
    member_list = ctx.message.mentions  # une liste d'objets
    # on regarde si le plus haut role de l'auteur du message est au dessus
    # du role (ou égal) au role DCT dans la hiérarchie
    counter = 0
    if ctx.author.top_role >= bot.role_dcteam:
        if member_list == []:
            pass
        else:
            for member in member_list:
                if bot.role_dcteam in member.roles:  # le counter c'est pour voir si tous les membres mentionnés
                    counter += 1
                await member.add_roles(bot.role_dcteam)  # sont dans la team, alors on n'affiche pas le message de bienvenue
            if counter == len(member_list):
                return None
            await ctx.send(content="Bienvenue dans la Team !")
    else:
        await ctx.send(content="Bien tenté mais tu n'as pas de pouvoir ici !")


@bot.command()
async def getcomics(ctx):
    user_input = get_command_input(ctx.message.content)
    title, url = getcomics_top_link(user_input)
    embed = discord.Embed(title=f"{title}", description="cliquez sur le titre pour télécharger votre comic", color=0x882640, url=url)
    await ctx.send(embed=embed)


@bot.command()
async def urban(ctx):
    user_input = get_command_input(ctx.message.content)
    # create object urban of class Urban
    urban = Urban_search(user_input)
    if urban.valid:
        title, meaning, example, search_url = urban.get_top_def()
        embed = discord.Embed(title=f"Definition of {title}", description=meaning, color=0x00FFFF, url=search_url)
        embed.add_field(name="Example", value=example, inline=False)
        embed.set_thumbnail(url=urban_logo)
    else:
        embed = discord.Embed(title=f"Definition of {user_input} doesn't exist")
    await ctx.send(embed=embed)


@bot.command()
async def clear(ctx):
    # on regarde si le plus haut role de l'auteur est supérieur
    # ou égal hiérarchiquement au role DCT
    if ctx.author.top_role >= bot.role_dcteam:
        nbr_msg = int(get_command_input(ctx.message.content))
        messages = await ctx.channel.history(limit=nbr_msg + 1).flatten()
        await ctx.channel.delete_messages(messages)
        await ctx.send(content=f"J'ai supprimé {nbr_msg} messages",
                       delete_after=5)
    else:
        await ctx.send(content=f"Tu n'as pas le pouvoir{ctx.author.mention} !")


@bot.command()
async def recrutement(ctx):
    embed = discord.Embed(title="Rejoins le team DCTrad !",
                          description="allez n'aies pas peur de cliquer et deviens un héros !",
                          color=0x0000FF, url=dctrad_recru)
    embed.set_thumbnail(url=dctradlogo)
    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx):
    user_input = get_command_input(ctx.message.content)
    title, url = youtube_top_link(user_input)
    await ctx.send(content=f"{title}\n{url}")


@bot.command()
async def youtubelist(ctx):
    user_input = get_command_input(ctx.message.content)
    duo = user_input.split(' ', 1)
    number = int(duo[0])
    query = duo[1]
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
        return message.author == ctx.author and (message.content == "cancel" or string_is_int(message.content))
    try:
        msg = await bot.wait_for("message", check=check, timeout=15)
        if msg.content == "cancel":
            await ctx.send("Annulé !", delete_after=5)
            await self_message.delete(delay=None)
            await ctx.message.delete(delay=2)
            await msg.delete(delay=1)
        else:
            num = int(msg.content)
            if num > 0 and num <= len(result):
                url = get_youtube_url(result[num - 1])
                await ctx.send(content=f"{url}")
                await ctx.message.delete(delay=2)
                await self_message.delete(delay=None)
                await msg.delete(delay=1)

    except asyncio.TimeoutError:
        await ctx.send("Tu as pris trop de temps pour répondre !", delete_after=5)
        await self_message.delete(delay=None)
        await ctx.message.delete(delay=2)


@bot.command()
async def comicsblog(ctx, num):
    list = get_comicsblog(num)
    embed = discord.Embed(title=f"les {num} derniers articles de comicsblog", color=0xe3951a)
    for l in list:
        embed.add_field(name=l.find('title').text, value=l.find('guid').text, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def kick(ctx):
    member_list = ctx.message.mentions
    if ctx.author.top_role >= bot.role_modo:
        for member in member_list:
            await member.kick()
    else:
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")


@bot.command()
async def ban(ctx):
    member_list = ctx.message.mentions
    if ctx.author.top_role >= bot.role_modo:
        for member in member_list:
            await member.ban(delete_message_days=3)
    else:
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")


@bot.command()
async def google(ctx):
    query = get_command_input(ctx.message.content)
    try:
        result = google_top_link(query)
        await ctx.send(content=f"{result['title']}\n {result['url']}")
    except TypeError:
        pass


@bot.command()
async def googlelist(ctx, num, *, args):
    result = search_google(args, num)
    embed = discord.Embed(title=f"Les {num} premiers résultats de la recherche", color=0x3b5cbe)
    for r in result:
        embed.add_field(name=r['title'], value=r['url'], inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def timer(ctx, numb, *, args):
    num = int(numb)
    await ctx.send(content=f"{ctx.author.mention} : timer enregistré !", delete_after=10)
    await asyncio.sleep(num, result=None, loop=None)
    await ctx.send(content=f"temps écoulé ! : {ctx.author.mention} {args}")


@bot.command()
async def roulette(ctx):
    if random.randrange(6) == 3:
        await ctx.send(content=f"Pan !")
        await ctx.send(content=snap_url, delete_after=4)
        await asyncio.sleep(2.4, result=None, loop=None)
        await ctx.author.kick()
    else:
        await ctx.send(content="*clic*....Tu restes vivant !")


@bot.command()
async def gif(ctx, name):
    if name == 'help':
        habile = []
        list_names = ""
        for key, value in my_giflist.gifs.items():
            if value['public']:
                habile.append(key + "\n")

            elif ctx.channel.category_id == dcteam_category_id:
                habile.append(key + "\n")
        for x in habile:
            list_names = list_names + x
        embed = discord.Embed(title="liste des gifs", description=list_names, color=0x000FF)
        await ctx.send(embed=embed)
    if my_giflist.get_gif(name) is not None:
        if my_giflist.get_gif(name)['public'] or ctx.channel.category_id == dcteam_category_id:
            gif_url = my_giflist.get_gif(name)['url']
            await ctx.send(content=gif_url)
    else:
        pass


@bot.command()
async def admin(ctx):
    embed = discord.Embed(color=0x0000FF)
    embed.add_field(name="gifadd", value="!gifadd <name> <url> <bool> (bool : public or private)", inline=False)
    embed.add_field(name="gifdelete", value="!gifdelete <name>", inline=False)
    if ctx.author.top_role > bot.guild.get_role(admin_id):
        await ctx.author.send(embed=embed)


@bot.command()
async def gifadd(ctx, name, url, bool):
    if ctx.author.top_role > bot.guild.get_role(admin_id):
        my_giflist.gif_add(name, url, bool)
    else:
        pass


@bot.command()
async def gifdelete(ctx, name):
    if ctx.author.top_role > bot.guild.get_role(admin_id):
        my_giflist.gif_delete(name)
    else:
        pass


@bot.command()
async def choose(ctx, *choices):
    if len(choices) < 1:
        return None
    await ctx.send(random.choice(choices))


@bot.command()
async def coinflip(ctx):
    await ctx.send(random.choice(["pile", "face"]))


@bot.command()
async def say(ctx, *, args):
    await ctx.message.delete()
    await ctx.send(content=args)


@bot.event
async def on_message(ctx):
    channel = ctx.channel
    # Find if custom command exist in dictionary
    for key, value in my_giflist.gifs.items():
        # Added simple hardcoded prefix
        command = '!' + key
        if ctx.content == command:
            if my_giflist.get_gif(key)['public'] or ctx.channel.category_id == dcteam_category_id:
                gif_url = my_giflist.get_gif(key)['url']
                await channel.send(gif_url)

bot.run(token)
