# IMPORTS
from discord.ext.commands import Bot
import os

# VARIABLES
bot = Bot(command_prefix='-')


# BOT IS READY
@bot.event
async def on_ready():
    print('All systems nominal.')


# IGNORE MESSAGES FROM BOT
@bot.event
async def on_message(m):
    if m.author == bot.user:
        return


bot.run(os.environ.get("BOT_TOKEN"))
