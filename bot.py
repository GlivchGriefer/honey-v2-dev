# IMPORTS
import os
import discord
import psycopg2
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands

# VARIABLES
load_dotenv()
token = os.environ["BOT_TOKEN"]
cid = os.environ["CLIENT_ID"]
oa2 = os.environ["CLIENT_SECRET"]
status = 'TEST STATUS'

bot = commands.Bot(command_prefix='•')


# BASE EVENTS ----------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    """
    TODO: DOCUMENTATION
    """
    # PRINT BOT INFORMATION TO CONSOLE
    print(f'\n• python 3.8.3')
    print(f'\n• Discord.py(Version: {discord.__version__})')
    print(f'\n•• Bot connected as {bot.user.name}')
    print(f'\n•• Bot ID: {bot.user.id}')
    print('\n••• All events and commands loaded •••')
    print('\n••• All systems nominal....')
    bot.remove_command('help')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="LFG Radio"))


# ADMIN COMMANDS / EVENTS ----------------------------------------------------------------------------------------------
@bot.command()
@commands.is_owner()
async def test(message):
    """
    TODO: DOCUMENTATION
    """
    print('\nTest successful!')
    await message.channel.send('Testing 1 2 3!')


@bot.event  # IGNORE MESSAGES FROM BOT | TRY COMMAND HANDLER
async def on_message(message):
    """
    TODO: DOCUMENTATION
    """
    # if the message is from the bot itself ignore it
    if message.author == bot.user:
        pass
    await bot.process_commands(message)


# ----------------------------------------------------------------------------------------------------------------------
@bot.command()
async def submit(ctx, *, arg):  # |!| COMPLETE MODULE WITH WORKING CODE
    """
   [D]
   """
    discord_id = ctx.message.author.id
    username = ctx.message.author
    link = arg

    sql = """INSERT INTO sys_monday(discord_id, username, link)
           VALUES(%s) RETURNING id;"""
    conn = None
    id = None

    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (discord_id, username, link))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        print('\nSubmitting ** to sys_monday')
        await ctx.message.channel.send("Submission received!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("\nThere was an error submitting to sys_monday!")
        await ctx.message.channel.send("There was an error submitting to sys_monday!")
    finally:
        if conn is not None:
            conn.close()


@bot.command()
async def a(ctx, *, arg):
    await discord.message.Message.delete(ctx.message)
    check_error = None

    # [Invite Link]
    em0 = discord.Embed(color=12190705)  # purple
    e0 = get(ctx.message.guild.emojis, name="xar2EDM")
    em0.title = str(e0) + " Speaker Honey Invite Link " + str(e0)
    em0.add_field(name="Invite to #rules-for-access:", value="discord.gg/fJhhkXn")

    # [QoneHead Announcement]
    em1 = discord.Embed(color=16098851)  # orange
    e1 = get(ctx.message.guild.emojis, name="QONE")
    role = ctx.guild.get_role(783796754189385808)
    em1.title = "Attention " + str(e1) + "Heads!"
    em1.set_image(url="https://media.discordapp.net/attachments/564008583411269633/794937189699026964/unknown.png")
    em1.description = f"{role.mention}" \
                      "\n\nThe time has almost come! Development for Share Your Song Monday submissions is going well " \
                      "and the work is almost complete. We may be able to submit to the bot before the next stream but " \
                      "I have to iron out more details still. I will need some of you to test submissions soon and I " \
                      "still need to do complete some basic functions like retrieving a list from the database and " \
                      "creating a re-submit command that replaces the current link for a user." \
                      "\n\nBelow is a preview of what's in progress and check out the rules channel for the new " \
                      "invite link embed." \
                      "\n\nIf anyone has any ideas or can think of any ways a bot can help people enjoy the server more" \
                      ", let me know!" \
                      "\n\n- " \
                      f"{ctx.author.mention}"

    # Initialize list of announcements [EMBEDS]
    an = [em0, em1]
    try:
        await ctx.message.channel.send(embed=an[int(arg)])

    except IndexError as error:
        check_error = True
        await ctx.message.channel.send("ERROR: " + str(error), delete_after=15)
        print("\nAnnounce Error: " + str(error))

    finally:
        if check_error is not True:
            print("\nAnnouncement #" + arg + " was successfully posted to " + str(ctx.message.channel))


# ----------------------------------------------------------------------------------------------------------------------

bot.run(os.environ["BOT_TOKEN"])
