# IMPORTS
import os
import discord
from discord.ext.commands import Bot
from Commands.CommandHandler import CommandHandler


# VARIABLES
from Commands.HelloCommand import hello_function

bot = Bot(command_prefix='-')
ch = CommandHandler(bot)


# BOT IS READY
@bot.event
async def on_ready():
    try:
        # PRINT BOT INFORMATION TO CONSOLE
        print(bot.user.name)
        print(bot.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))
        print('All systems nominal.')

    except Exception as e:
        print(e)


# IGNORE MESSAGES FROM BOT | TRY COMMAND HANDLER
@bot.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == bot.user:
        pass
    else:

        # try to evaluate with the command handler
        try:
            await ch.command_handler(message)

        # message doesn't contain a command trigger
        except TypeError as e:
            pass

        # generic python error
        except Exception as e:
            print(e)

# ADD COMMANDS ---------------------------------------------------------------------------------------------------------
# HELLO
ch.add_command({
    # IF MESSAGE STARTS WITH TRIGGER
    'trigger': '-hello',

    # CALL MAIN FUNCTION
    'function': hello_function,

    # NUMBER OF ARGUMENTS NEEDED
    'args_num': 1,

    # NAME OF THE ARGUMENT
    'args_name': ['string'],

    # DESCRIBE WHAT FUNCTION DOES
    'description': 'Will respond hello to the caller and show arg 1'
})
# ADD COMMANDS ---------------------------------------------------------------------------------------------------------

bot.run(os.environ["BOT_TOKEN"])
