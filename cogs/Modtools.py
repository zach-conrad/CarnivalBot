import json

import discord
from discord.ext import commands
from discord import app_commands


class Modtools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modtools.py is ready.")

    @commands.command(aliases=["purge", "c"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.author.send(f"Cleared {count} messages.")

    # Command to kick members #TODO Make slash command.
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, modreason):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Kicked", value=f"{member.mention}", inline=False)
        conf_embed.add_field(name="Reason", value=modreason, inline=False)
        conf_embed.add_field(name="Punisher", value=ctx.author.name, inline=False)
        await ctx.send(embed=conf_embed)

    # Command to ban members #TODO Make slash command.
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, modreason):
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Banned", value=f"{member.mention}", inline=False)
        conf_embed.add_field(name="Reason", value=modreason, inline=False)
        conf_embed.add_field(name="Punisher", value=ctx.author.name, inline=False)
        await ctx.send(embed=conf_embed)

    # Command to unban members #TODO Make slash command.
    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Unbanned", value=f"{userId.mention}", inline=False)
        conf_embed.add_field(name="Issuer", value=ctx.author.name, inline=False)
        await ctx.send(embed=conf_embed)

    # Mute Command TODO - Use it inside of a database, and add option for times.
    @app_commands.command(name="setmuterole", description="sets the muted player role")
    @app_commands.checks.has_permissions(administrator=True)
    async def setmuterole(self, interaction, role: discord.Role):
        with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "r") as f:
            mute_role = json.load(f)

            mute_role[str(interaction.guild.id)] = role.name

        # Checks if there is any one in the mute roles.
        with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "w") as f:
            json.dump(mute_role, f, indent=4)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Mute role set!", value=f"Mute role has been set to {role.mention}", inline=False)

        await interaction.response.send_message(embed=conf_embed)

    @app_commands.command(name="mute", description="mute a player for a designated period of time")
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction, member: discord.Member, reason: str):
        with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "r") as f:
            role = json.load(f)

            mute_role = discord.utils.get(interaction.guild.roles, name=role[str(interaction.guild.id)])

        await member.add_roles(mute_role)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Muted", value=f"{member}", inline=False)
        conf_embed.add_field(name="Reason", value=f"{reason}", inline=False)
        conf_embed.add_field(name="Issuer", value=f"{interaction.user}", inline=False)

        await interaction.response.send_message(embed=conf_embed)

    @app_commands.command(name="unmute", description="unmute a player")
    @app_commands.checks.has_permissions(administrator=True)
    async def unmute(self, interaction, member: discord.Member, reason: str):
        with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "r") as f:
            role = json.load(f)

            mute_role = discord.utils.get(interaction.guild.roles, name=role[str(interaction.guild.id)])

        await member.remove_roles(mute_role)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="UnMuted", value=f"{member}", inline=False)
        conf_embed.add_field(name="Reason", value=f"{reason}", inline=False)
        conf_embed.add_field(name="Issuer", value=f"{interaction.user}", inline=False)

        await interaction.response.send_message(embed=conf_embed)


async def setup(client):
    await client.add_cog(Modtools(client))
