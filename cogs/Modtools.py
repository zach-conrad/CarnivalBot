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

    @app_commands.command(name="purge", description="Clear a certain number of messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction, count: int):
        await interaction.channel.purge(limit=count)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Messages Cleared", value= f"{count}", inline=False)
        conf_embed.add_field(name="Issuer", value=f"{interaction.user}", inline=False)

        await interaction.response.send_message(embed=conf_embed)

    @app_commands.command(name="kick", description="Kick a member from the discord server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction, member: discord.Member, modreason : str):
        await interaction.guild.kick(member)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Kicked", value=f"{member.mention}", inline=False)
        conf_embed.add_field(name="Reason", value=modreason, inline=False)
        conf_embed.add_field(name="Issuer", value=interaction.user, inline=False)

        await interaction.response.send_message(embed=conf_embed)

    @app_commands.command(name="ban", description="Ban a member from the discord server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction, member: discord.Member, modreason : str):
        await interaction.guild.ban(member)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Banned", value=f"{member.mention}", inline=False)
        conf_embed.add_field(name="Reason", value=modreason, inline=False)
        conf_embed.add_field(name="Punisher", value=interaction.user, inline=False)
        await interaction.response.send_message(embed=conf_embed)

    # Command to unban members #TODO Make slash command.
    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction, userId: discord.User):
        user = discord.Object(id=userId)
        await interaction.guild.unban(user)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Unbanned", value=f"{userId.mention}", inline=False)
        conf_embed.add_field(name="Issuer", value=interaction.user, inline=False)
        await interaction.send(embed=conf_embed)

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
