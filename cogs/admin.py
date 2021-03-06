import os

import discord
import psycopg2
from discord.ext import commands


class AdminCommands(commands.Cog):
    """
    Admin commands for admins
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        db_database = os.environ["AJU_DB_DATABASE"]
        db_user = os.environ["AJU_DB_USER"]
        db_password = os.environ["AJU_DB_PASSWORD"]
        db_host = os.environ["AJU_DB_HOST"]
        db_port = os.environ["AJU_DB_PORT"]

        try:
            self.db = psycopg2.connect(
                database=db_database,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
        except psycopg2.OperationalError as error:
            print(error)

        self.cursor = self.db.cursor()

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def cls(self, ctx: commands.Context, amount: int = 2):

        if amount == 1:
            embed = discord.Embed(
                description=f"cleared `{amount}` message in {ctx.channel.mention}",
                colour=discord.Colour(0xE9ACFD),
            )
        else:
            embed = discord.Embed(
                description=f"cleared `{amount}` messages in {ctx.channel.mention}",
                colour=discord.Colour(0xE9ACFD),
            )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result_1 = self.cursor.fetchone()
        if result_1 is None:
            return
        else:
            audit_ch = self.bot.get_channel(id=int(result_1[0]))
            await audit_ch.send(embed=embed)

        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(f"Aju `{amount}` message delete kollin.")

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str = ""):
        embed = discord.Embed(
            title=f"kicked **{user}** from {ctx.guild}.",
            description=reason,
            colour=discord.Colour(0xE9ACFD),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await user.kick(reason=reason)
        await ctx.send(f"Bye bye {user.mention}.")

        self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        if result is None:
            return
        else:
            audit_ch = self.bot.get_channel(id=int(result[0]))
            await audit_ch.send(embed=embed)

    @commands.command(aliases=["reqinv"])
    async def req_invite(self, ctx: commands.Context):
        global inv_author
        inv_author = ctx.author
        global auth_ch
        auth_ch = ctx.channel

        self.cursor.execute(f"SELECT ch_id_admin FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        if result is None:
            await ctx.send("Please set admin channel first. Use `.set` for more info.")
        else:
            admin_ch = self.bot.get_channel(id=int(result[0]))
            await ctx.channel.send("Requesting invite link from admins...")
            await admin_ch.send(
                f"{inv_author.mention} is requesting an invite link for {ctx.channel.mention}. Use `.confirm` or `.deny`"
            )

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def confirm(self, ctx: commands.Context):
        link = await ctx.channel.create_invite(max_age=86400, max_uses=5)
        dm = self.bot.get_user(inv_author.id)

        embed = discord.Embed(
            title="**confirmed** an invite link request.",
            description=f"from **{inv_author}** for {auth_ch.mention}",
            colour=discord.Colour(0xE9ACFD),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await auth_ch.send(
            f"Invite link requested by {inv_author.mention} was **confirmed**. Pls check your dms for the link."
        )
        await dm.send(f"{link}")

        self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        if result is None:
            return
        else:
            audit_ch = self.bot.get_channel(id=int(result[0]))
            await audit_ch.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def deny(self, ctx: commands.Context):
        embed = discord.Embed(
            title="**denied** an invite link request.",
            description=f"from **{inv_author}** for {auth_ch.mention}",
            colour=discord.Colour(0xE9ACFD),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await auth_ch.send(f"Invite link requested by {inv_author.mention} was **denied**.")

        self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        if result is None:
            return
        else:
            audit_ch = self.bot.get_channel(id=int(result[0]))
            await audit_ch.send(embed=embed)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
