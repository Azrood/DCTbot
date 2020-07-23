"""Store secret tokens and stuff here.

Rename file in 'secret.py'
"""

import os
from dotenv import load_dotenv

# Parse a .env file and then load all the variables found as environment variables.
load_dotenv()


token = os.getenv("DISCORD_TOKEN")  # str
main_guild_id = int(os.getenv("MAIN_GUILD_ID"))  # int
dcteam_role_id = 376097209738985483  # int
modo_role_id = 376097033053798430  # int
token_youtube = os.getenv("YOUTUBE_TOKEN")  # str
DEVELOPER_CX = os.getenv("GOOGLE_DEVELOPER_CX")  # str

dcteam_category_id = 376101275898609664  # int

admin_role = ["Dieu du Discord", "Administrateur", "I\'ve got the power"]  # list of str
staff_role = ["DCT-TEAM", "Modérateurs", "Coordinateur", "Administrateur", "Dieu du Discord", "Canard du Discord"]  # noqa: E501
mods_role = ["Modérateurs", "Coordinateur", "Administrateur", "Dieu du Discord", "Dominatrix Imperiosa"]  # noqa: E501

react_role_msg_id = 647194400329302019

logging_webhook_url = os.getenv("LOGS_WEBHOOK")
