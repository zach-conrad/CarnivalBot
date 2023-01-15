import discord
from discord.ext import commands
from discord import app_commands
import json

class Modtools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modtools.py is ready.")

    @commands.command(aliases= ["purge", "c"])
    @commands.has_permissions(manage_messages= True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit= count)
        await ctx.author.send(f"Cleared {count} messages.")

    #Command to kick members #TODO Make slash command.
    @commands.command()
    @commands.has_permissions(kick_members= True)
    async def kick(self, ctx, member: discord.Member, modreason):
        await ctx.guild.kick(member)


        conf_embed = discord.Embed(title= "Success!", color=discord.Color.green())
        conf_embed.add_field(name= "Kicked", value= f"{member.mention}", inline= False)
        conf_embed.add_field(name= "Reason", value= modreason, inline= False)
        conf_embed.add_field(name="Punisher", value= ctx.author.name, inline= False)
        await ctx.send(embed= conf_embed)

    #Command to ban members #TODO Make slash command.
    @commands.command()
    @commands.has_permissions(ban_members= True)
    async def ban(self, ctx, member: discord.Member, modreason):
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title= "Success!", color=discord.Color.green())
        conf_embed.add_field(name= "Banned", value= f"{member.mention}", inline= False)
        conf_embed.add_field(name= "Reason", value= modreason, inline= False)
        conf_embed.add_field(name="Punisher", value= ctx.author.name, inline= False)
        await ctx.send(embed= conf_embed)

    #Command to unban members #TODO Make slash command.
    @commands.command(name= "unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members= True)
    async def unban(self, ctx, userId):
        user = discord.Object(id= userId)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title= "Success!", color=discord.Color.green())
        conf_embed.add_field(name= "Unbanned", value= f"{userId.mention}", inline= False)
        conf_embed.add_field(name="Issuer", value= ctx.author.name, inline= False)
        await ctx.send(embed= conf_embed)

    #Mute Command TODO - Use it inside of a database







async def setup(client):
    await client.add_cog(Modtools(client))

