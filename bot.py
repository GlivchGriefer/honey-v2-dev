# IMPORTS
import os
import re
from random import randrange

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

bot = commands.Bot(command_prefix='-')


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
@bot.command()  # |•| Beautify embed
async def sys(ctx, *, arg):
    """
   [D]
    :param arg:
    :param ctx:
   """
    discord_id = ctx.message.author.id
    username = ctx.message.author.display_name
    link = arg
    embed_s = discord.Embed(color=discord.Color.green())

    sql = """INSERT INTO sys_monday(discord_id, username, link)
           VALUES(%s, %s, %s) RETURNING id;"""
    sql2 = """SELECT id, username, link FROM sys_monday ORDER BY id"""
    conn = None
    id = None

    if "qonehead" in [y.name.lower() for y in ctx.message.author.roles]:  # |•| CHANGE ROLE TO TWITCH SUB or list
        # ATTEMPT SUBMISSION
        try:
            # connect to the PostgreSQL database
            conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
            # set auto commit to false
            conn.autocommit = True
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (discord_id, username, link,))
            # get the generated id back
            submission_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()

            # report success in logs and channel
            print('\n' + username + ' submitted to [sys_monday]  • • •  ID: ' + str(submission_id))
            embed_s.title = "Success!"
            embed_s.description = "Your submission has been accepted!"
            await discord.message.Message.delete(ctx.message)  # DELETE CMD MSG

            if str(ctx.channel) == "qone-zone2":  # |•| SET TO CORRECT CHANNEL
                await ctx.channel.purge(limit=1)  # Delete current list
                await ctx.channel.send(embed=list_submissions(sql2, ctx))  # |•| WILL NOT AUTO-DELETE
            else:
                await ctx.channel.send("ONLY USE THAT COMMAND IN qone-zone2", delete_after=15)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("\nThere was an error submitting to sys_monday!")
            await ctx.message.channel.send("There was an error submitting to sys_monday!"
                                           + "\n***" + str(error) + "***", delete_after=15)
        finally:
            print("\n-- #" + str(submission_id) + " SUCCESS " + str(ctx.message.author))
            if conn is not None:
                conn.close()


# list_submissions |!| beautify formatting MAKE COMMAND FOR THIS ONLY
def list_submissions(sql2, ctx):
    """
    [D]
    :param ctx:
    :param sql2:
    :return:
    """
    listsize = 0
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql2)

        results =[]
        one_submission = []
        submissionlist = []
        for result in cur:
            results.append(result)
        cur.close()
        for entity in results:
            submission = str(entity)[str(entity).find('[')+1:str(entity).find(']')]
            print(submission)
            one_submission.append(submission.split(','))
        for _ in one_submission:
            tl = str(_).split(',')
            o1 = '\n' + re.sub("[('[]", '', str(tl[0]))
            o2 = '\t' + re.sub("[\'\"]", '', str(tl[1]))
            o3 = '\t' + re.sub("[]'\"]", '', str(tl[2]))
            submissionlist.append(o1 + o2 + o3)

        e_desc = " ".join(submissionlist)
        print(e_desc)
        embed_list = discord.Embed(color=discord.colour.Color.value(700400), description=e_desc)
        list_as_string = str(embed_list)
        listsize = len(list_as_string)
        # CATCH max embed length (100 chars)
        if listsize <= 100:
            if not a:
                first = discord.Embed(color=discord.Color.green())
                first.title = "Submission success!"
                return first
            else:
                embed_list.title = "Current submissions: " + str(cur.rowcount)
                return embed_list
        else:
            print("\n∟ EXCEEDED")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # print("•mÖÐEQ©:←↓↓↑→→∟§&←↓∟UA-↓Ü~→○○○○")
        print("\nEMBED SENT to \"" + str(ctx.channel) + "\"\n  ∟" + str(listsize) + "chars")


@bot.command()  # Announce
async def a(ctx, *, arg):  # |!| optimize using randint and for loop
    await discord.message.Message.delete(ctx.message)
    check_error = None

    # [Invite Link]
    em0 = discord.Embed(color=12190705)  # purple
    e0 = get(ctx.message.guild.emojis, name="HACKS")
    em0.title = str(e0) + " Speaker Honey Invite Link " + str(e0)
    em0.add_field(name="Invite to #rules-for-access:", value="discord.gg/fJhhkXn")

    # [QoneHead Announcement]
    em1 = discord.Embed(color=16098851)  # orange
    e1 = get(ctx.message.guild.emojis, name="FeelsLagMan")
    role = ctx.guild.get_role(559692297642442764)  # @Owner
    em1.title = "Attention " + str(e1) + "Heads!"
    em1.set_image(url="https://media.discordapp.net/attachments/564008583411269633/794937189699026964/unknown.png")
    em1.description=f"{role.mention}" \
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
        await ctx.message.channel.send(embed=an[int(arg)], delete_after=45)  # |!| DOES NOT AUTO-DELETE

    except IndexError as error:
        check_error = True
        await ctx.message.channel.send("ERROR: " + str(error), delete_after=5)
        print("\nAnnounce Error: " + str(error))

    finally:
        if check_error is not True:
            print("\nAnnouncement #" + arg + " was successfully posted to " + str(ctx.message.channel))


@bot.command()  # Generate a random number
async def rng(ctx):
    await discord.message.Message.delete(ctx.message)
    # parameter integer between 1 and 10
    value = randrange(1, 10)
    await ctx.message.channel.send(value, delete_after=5)


@bot.command()  # delete messages
async def d(ctx, arg: int):
    await discord.message.Message.delete(ctx.message)
    await ctx.channel.purge(limit=arg)


@bot.command()
async def cr(ctx):  # check role
    await discord.message.Message.delete(ctx.message)
    if "user" in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.message.channel.send("Success!", delete_after=5)
    else:
        await ctx.message.channel.send("FAIL", delete_after=5)
# ----------------------------------------------------------------------------------------------------------------------

bot.run(os.environ["BOT_TOKEN"])
