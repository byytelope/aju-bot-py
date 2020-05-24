import discord
import psycopg2
import datetime
from discord.ext import commands

default_role = 'Fukushima Daichi'

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # self.db = psycopg2.connect(
        #     database="d5gmd9koh5vegt", 
        #     user="htildhifgbegjh", 
        #     password="b4b03250555235feb27acab0d9abbf0be289a0b08cc265478be37bcbd87c5c8c", 
        #     host="ec2-52-202-22-140.compute-1.amazonaws.com", 
        #     port="5432")
        # self.cursor = self.db.cursor()
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=default_role)
        await member.add_roles(role)
        print(f'{member} was given {role}')
        
        embed = discord.Embed(description = f'Welcome to Bionic {member.mention}!', colour = discord.Colour.blurple())
        embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
        embed.set_thumbnail(url=f'{member.avatar_url}')
        embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
        embed.timestamp = datetime.datetime.now()

        welc_ch = self.bot.get_channel(592074944217612298)
        await welc_ch.send(embed=embed)
        

        # self.cursor.execute(f'SELECT ch_id_welcome FROM main WHERE guild_id = {str(member.guild.id)}')
        # result = self.cursor.fetchone()
        # if result is None:
        #     return
        # else:
        #     self.cursor.execute(f'SELECT welc_text FROM main WHERE guild_id = {str(member.guild.id)}')
        #     result_1 = self.cursor.fetchone()

        #     embed = discord.Embed(description = f'{str(result_1[0])}', colour = discord.Colour.blurple())
        #     embed.set_thumbnail(url=f'{member.avatar_url}')
        #     embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
        #     # embed.timestamp = datetime.datetime.now()

        #     welc_ch = self.bot.get_channel(id=int(result[0]))
        #     await welc_ch.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))