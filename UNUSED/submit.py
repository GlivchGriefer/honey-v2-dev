import os
from discord.ext import commands
import psycopg2


class Submit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def submit(self, ctx, *, arg):
        """
        TODO: DOCUMENTATION
        """
        discord_id = ctx.message.author.id
        username = ctx.message.author
        link = arg

        sql ="""INSERT INTO sys_monday(discord_id, username, link)
                VALUES(%s) RETURNING id;"""
        conn = None
        id = None

        try:
            # read database configuration
            params = os.config["DBCONNECT"]
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
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
            ctx.reply("Submission received!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("\nThere was an error submitting to sys_monday!")
        finally:
            if conn is not None:
                conn.close()


def setup(bot):
    bot.add_cog(Submit(bot))
