# IMPORTS
import os
import re
from random import randrange

import discord
import psycopg2
from discord import guild, Guild
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands

# VARIABLES
load_dotenv()
token = os.environ["BOT_TOKEN"]
cid = os.environ["CLIENT_ID"]
oa2 = os.environ["CLIENT_SECRET"]
status = 'TEST STATUS'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='-', intents=intents)


# BASE EVENTS ------------------------------------------------------------------
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

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="Together All Night"))


# ADMIN COMMANDS / EVENTS ------------------------------------------------------
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


# ------------------------------------------------------------------------------
class KeepClean(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, msg):
        channel = msg.channel
        if msg.author == bot.user:
            pass
        if str(channel) == "share-your-song":
            if not msg.author == bot.user and not str(msg.content).startswith('-sys'):
                await discord.message.Message.delete(msg)
            else:
                pass


# ------------------------------------------------------------------------------
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

    if "fortunate one" or "admin" in [y.name.lower() for y in ctx.message.author.roles]:
        # ATTEMPT SUBMISSION
        try:
            if str(ctx.channel) == "share-your-song":
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
                sl = list_submissions(sql2, ctx)

                await discord.message.Message.delete(ctx.message)  # DELETE CMD MSG
                nos = len(sl)
                if nos > 20:
                    await ctx.channel.purge(limit=2)  # IF THERE ARE TWO LISTS
                else:
                    await ctx.channel.purge(limit=1)  # Delete ONE list

                str1 = ''.join(sl[:19])
                str2 = ''.join(sl[19:])
                e1 = discord.Embed(color=discord.colour.Colour.from_rgb(112, 4, 0),
                                   description=str1, title="Current submissions: " + str(len(sl)))
                e2 = discord.Embed(color=discord.colour.Colour.from_rgb(112, 4, 0),
                                   description=str2)

                # SEND MESSAGE(S)
                await ctx.channel.send(embed=e1)
                if len(str2) > 0:
                    await ctx.channel.send(embed=e2)

            else:
                await ctx.channel.send("ONLY USE THAT COMMAND IN "
                                       "share-your-song", delete_after=15)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("\nThere was an error submitting to sys_monday!")
            await ctx.message.channel.send("There was an error submitting to "
                                           "Share Your Song Monday!"
                                           + "\n***" + str(error) + "***"
                                           , delete_after=15)
        finally:
            print("\n-- #" + str(submission_id) + " SUCCESS " + str(ctx.message.
                                                                    author))
            if conn is not None:
                conn.close()


# list_submissions |!| beautify formatting
def list_submissions(sql2, ctx):
    """
    [D]
    :param ctx:
    :param sql2:
    :return:
    """
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql2)

        results = []
        one_submission = []
        submissionlist = []
        for result in cur:
            results.append(result)
        cur.close()
        for entity in results:
            submission = str(entity)[str(entity).find('[') + 1:str(entity)
                .find(']')]
            print(submission)
            one_submission.append(submission.split(','))
        for _ in one_submission:
            tl = str(_).split(',')
            o1 = '\n' + re.sub("[('[]", '', str(tl[0]))
            o2 = '\t' + re.sub("[\'\"]", '', str(tl[1]))
            o3 = "\t[link](" + re.sub("[]'\"]", '', str(tl[2]) + ")")
            submissionlist.append(o1 + o2 + o3)
        return submissionlist

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # print("•mÖÐEQ©:←↓↓↑→→∟§&←↓∟UA-↓Ü~→○○○○")
        print('list_submissions |SUCCESS|')


@bot.command()  # Show submissions (sys)
async def show(ctx):
    await discord.message.Message.delete(ctx.message)  # DELETE CMD MSG

    sql = """SELECT id, username, link FROM sys_monday ORDER BY id"""
    sl = list_submissions(sql, ctx)

    str1 = ''.join(sl[:19])
    str2 = ''.join(sl[19:])
    e1 = discord.Embed(color=discord.colour.Colour.from_rgb(112, 4, 0),
                       description=str1, title="Current submissions: "
                                               + str(len(sl)))
    e2 = discord.Embed(color=discord.colour.Colour.from_rgb(112, 4, 0),
                       description=str2)

    # SEND MESSAGE(S)
    await ctx.channel.send(embed=e1)
    if len(str2) > 0:
        await ctx.channel.send(embed=e2)


@bot.command()  # Announce
async def a(ctx, *, arg):
    await discord.message.Message.delete(ctx.message)
    check_error = None

    # NO SUBMISSIONS
    em0 = discord.Embed(color=discord.colour.Colour.from_rgb(112, 4, 0),
                        description="Submit using -sys followed by your link")
    em0.title = "Current submissions: 0"

    # sys rules
    em1_d = "**Please do not post anything but the submission command to this channel.**" \
            "\n\nSimply type -sys 'the link to your song'\nEx) -sys https://soundcloud.com/" \
            "\n\nRules:" \
            "\n[1] Only submit works in progress, or remixes by YOU not someone else." \
            "\n[2] No already released songs, only works in progress. " \
            "This isn't share my EP time, it's meant to give feedback and productive guidance that can applied to" \
            " tracks still in progress (please only link your new releases in #got-a-release-post-it-here )." \
            "\n[3] Only one track per artist each stream." \
            "\n[4] Finally, please be present when Speaker Honey is approaching your track during stream." \
            "\n\nTune in Mondays at 7:30 PM PST" \
            "\n\n*All messages in this channel " \
            "will be deleted immediately. You will know if your submission is successful.*" \
            "\n**DO NOT SUBMIT MORE THAN ONCE PER WEEK**"
    em1 = discord.Embed(color=discord.colour.Colour.from_rgb(112, 4, 0),
                        description=em1_d)
    # Initialize list of announcements [EMBEDS]
    an = [em0, em1]
    try:
        await ctx.message.channel.send(embed=an[int(arg)])

    except IndexError as error:
        check_error = True
        await ctx.message.channel.send("ERROR: " + str(error), delete_after=5)
        print("\nAnnounce Error: " + str(error))

    finally:
        if check_error is not True:
            print("\nAnnouncement #" + arg + " was successfully posted to "
                  + str(ctx.message.channel))


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


@bot.command()  # delete sys submission
async def ds(ctx, arg: int):
    await discord.message.Message.delete(ctx.message)
    number = arg
    sql = """DELETE FROM table_1 WHERE id = %s;"""
    conn = None
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql, number)
        conn.commit()
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        print('\nSubmission #' + str(number)
              + ' successfully deleted from database!')
        ctx.message.channel.send('Submission #' + str(number)
                                 + ' successfully deleted from database!'
                                 , delete_after=5)
        if conn is not None:
            conn.close()


@bot.command()
async def rr(ctx):  # check role
    """
    [D]
    :param ctx:
    """
    await discord.message.Message.delete(ctx.message)
    removal_failures = 0
    # await ctx.message.channel.send("Current number of members: "
    #                                + str(num_of_members))
    good_role = get(ctx.guild.roles, name="Fortunate One")
    bad_role = get(ctx.guild.roles, name="READ THE RULES")

    for member in ctx.guild.members:
        roles = member.roles
        if bad_role and good_role in roles:
            try:
                await member.remove_roles(bad_role)
            except:
                removal_failures += 1
    if removal_failures != 0:
        await ctx.send(f"Couldn't remove the role from {removal_failures}"
                       " members.")

# ------------------------------------------------------------------------------
bot.add_cog(KeepClean(bot))
bot.run(token)
