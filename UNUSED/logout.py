import asyncio
from discord.ext import commands
import discord

client = discord.client


class Logout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @commands.command(pass_context=True)
        async def logout(ctx):
            """
            TODO: DOCUMENTATION
            """

            await client.close()
            await ctx.channel.send('Attempting to logout...')
            print('\n• • • Attempting to log out • • •')
            message = await ctx.channel.send('Attempting to logout...')
            await asyncio.sleep(3)
            await bot.delete_message(message)
            await asyncio.sleep(4)


def setup(bot):
    bot.add_cog(Logout(bot))

