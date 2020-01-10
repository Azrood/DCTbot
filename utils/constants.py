#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Constants."""

# Emojis
left_triangle = "\U000025c0"
right_triangle = "\U000025b6"

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

greeting_list = [
    "Bonjour tout le monde !",
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
