import os

import discord
import psycopg2
from discord.ext import commands


class Set(commands.Cog):
    """
    Class for setting guild specific vars
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
        except psycopg2.OperationalError as db_error:
            print(db_error)

        self.cursor = self.db.cursor()

    @commands.command()
    @commands.is_owner()
    async def prtable(self, ctx: commands.Context):
        self.cursor.execute("SELECT * FROM main;")
        result = self.cursor.fetchall()
        print(result)

    @prtable.error
    async def on_prtable_error(self, ctx: commands.Context, error: commands.errors):
        if isinstance(error, commands.NotOwner):
            owner = self.bot.get_user(367686193242177536)
            await ctx.send(f"Sorry only {owner.mention} can use this command.")

    @commands.command()
    @commands.is_owner()
    async def droptable(self):
        self.cursor.execute("DROP TABLE IF EXISTS main;")
        self.db.commit()

    @droptable.error
    async def on_droptable_error(self, ctx: commands.Context, error: commands.errors):
        if isinstance(error, commands.NotOwner):
            owner = self.bot.get_user(367686193242177536)
            await ctx.send(f"Sorry only {owner.mention} can use this command.")

    @commands.group(invoke_without_command=True)
    async def set(self, ctx: commands.Context):
        embed = discord.Embed(title="set **<command>**", colour=discord.Colour(0xE9ACFD))
        embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.add_field(name="roleid", value="Set message id for role reactions.", inline=False)
        embed.add_field(
            name="welctext",
            value="Set welcome text. Available variables: \n`{mention}` (mentions member), \n`{user}` (member name without mentioning), \n`{guild}` (name of guild)",
            inline=False,
        )
        embed.add_field(name="welcch", value="Set welcome channel.", inline=False)
        embed.add_field(name="auditch", value="Set audit channel.", inline=False)
        embed.add_field(name="adminch", value="Set admin channel.", inline=False)
        embed.add_field(name="generalch", value="Set general channel.", inline=False)
        embed.add_field(name="defaultrole", value="Set the default role given to new users.", inline=False)
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @set.command(aliases=["roleid"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_msg_id_role(self, ctx: commands.Context, *, role_id: int):
        self.cursor.execute(f"SELECT msg_id_reaction FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        sql = None

        if result is None:
            sql = f"INSERT INTO main (guild_id, msg_id_reaction) VALUES ( ('{str(ctx.guild.id)}'), ('{str(role_id)}') )"
            await ctx.send("Message for role reactions has been set.")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description="set message for role reactions",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        elif result is not None:
            sql = f"UPDATE main SET msg_id_reaction = ('{str(role_id)}') WHERE guild_id = ('{str(ctx.guild.id)}')"
            await ctx.send("Message for role reactions has been changed.")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description="changed message for role reactions",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()

    @set.command(aliases=["welctext"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_welc_text(self, ctx: commands.Context, *, welc_text: str):

        self.cursor.execute(f"SELECT welc_text FROM main WHERE guild_id  = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        sql = None

        if result is None:
            sql = f"INSERT INTO main (guild_id, welc_text) VALUES ( ('{str(ctx.guild.id)}'), ('{welc_text}')"
            await ctx.send(
                f"""
                Welcome text has been set to **"{welc_text}"**
                """
            )

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f'set welcome text to **"{welc_text}"**',
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        elif result is not None:
            sql = f"UPDATE main SET welc_text = ('{welc_text}') WHERE guild_id = ('{str(ctx.guild.id)}')"
            await ctx.send(
                f"""
                Welcome text has been changed to "{welc_text}"
                """
            )

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f'changed welcome text to **"{welc_text}"**',
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()

    @set.command(aliases=["welcch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_welc_ch(self, ctx: commands.Context, welc_ch: discord.TextChannel):
        self.cursor.execute(f"SELECT ch_id_welcome FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        sql = None

        if result is None:
            sql = f"INSERT INTO main (guild_id, ch_id_welcome) VALUES ( ('{str(ctx.guild.id)}'), ('{welc_ch.id}') )"
            await ctx.send(f"Welcome channel has been set to {welc_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"set welcome channel to {welc_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        elif result is not None:
            sql = f"UPDATE main SET ch_id_welcome = ('{welc_ch.id}') WHERE guild_id = ('{str(ctx.guild.id)}')"
            await ctx.send(f"Welcome channel has been changed to {welc_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"changed welcome channel to {welc_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()

    @set.command(aliases=["auditch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_audit_ch(self, ctx: commands.Context, audit_ch: discord.TextChannel):
        self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        sql = None

        if result is None:
            sql = f"INSERT INTO main (guild_id, ch_id_audit) VALUES ( ('{str(ctx.guild.id)}'), ('{audit_ch.id}') )"
            await ctx.send(f"Audit channel has been set to {audit_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"set audit channel to {audit_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        elif result is not None:
            sql = f"UPDATE main SET ch_id_audit = ('{audit_ch.id}') WHERE guild_id = ('{str(ctx.guild.id)}')"
            await ctx.send(f"Audit channel has been changed to {audit_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"changed audit channel to {audit_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()

    @set.command(aliases=["adminch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_admin_ch(self, ctx: commands.Context, admin_ch: discord.TextChannel):
        self.cursor.execute(f"SELECT ch_id_admin FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        sql = None

        if result is None:
            sql = f"INSERT INTO main (guild_id, ch_id_admin) VALUES ( ('{str(ctx.guild.id)}'), ('{admin_ch.id}') )"
            await ctx.send(f"Admin channel has been set to {admin_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"set admin channel to {admin_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        elif result is not None:
            sql = f"UPDATE main SET ch_id_admin = ('{admin_ch.id}') WHERE guild_id = ('{str(ctx.guild.id)}')"
            await ctx.send(f"Admin channel has been changed to {admin_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"changed admin channel to {admin_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()

    @set.command(aliases=["generalch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_general_ch(self, ctx: commands.Context, general_ch: discord.TextChannel):
        self.cursor.execute(f"SELECT ch_id_general FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        sql = None

        if result is None:
            sql = f"INSERT INTO main (guild_id, ch_id_general) VALUES ( ('{str(ctx.guild.id)}'), ('{general_ch.id}') )"
            await ctx.send(f"General channel has been set to {general_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"set general channel to {general_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        elif result is not None:
            sql = f"UPDATE main SET ch_id_general = ('{general_ch.id}') WHERE guild_id = ('{str(ctx.guild.id)}')"
            await ctx.send(f"General channel has been changed to {general_ch.mention}")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description=f"changed general channel to {general_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()

    @set.command(aliases=["defaultrole"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_role_id_default(self, ctx: commands.Context, *, role_id: int):
        self.cursor.execute(f"SELECT role_id_default FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result = self.cursor.fetchone()
        sql = None

        if result is None:
            sql = f"INSERT INTO main (guild_id, role_id_default) VALUES ( ('{str(ctx.guild.id)}'), ('{str(role_id)}') )"
            await ctx.send("Default role has been set.")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description="set default role",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        elif result is not None:
            sql = f"UPDATE main SET role_id_default = ('{str(role_id)}') WHERE guild_id = ('{str(ctx.guild.id)}')"
            await ctx.send("Default role has been changed.")

            self.cursor.execute(f"SELECT ch_id_audit FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
            result_1 = self.cursor.fetchone()
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(id=int(result_1[0]))

                embed = discord.Embed(
                    description="changed default role",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()


def setup(bot):
    bot.add_cog(Set(bot))
