import discord
from discord.ext import commands
from discord import app_commands, Embed


class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Embed.py is ready.")

    # Creates an embed.
    @app_commands.command(name="embed", description="Send an embed.")
    @commands.has_permissions(administrator=True)
    async def embed(self, interaction=discord.Interaction):
        embed_message = discord.Embed(title="title", description="Description of the embed",
                                      color=discord.Color.dark_red())

        embed_message.set_author(name=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)
        embed_message.add_field(name="Field name", value="Field Value", inline=False)
        embed_message.set_image(url=interaction.user.avatar)
        embed_message.set_thumbnail(url=interaction.user.avatar)
        embed_message.set_footer(text="This is the footer.", icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=embed_message)


async def setup(client):
    await client.add_cog(Embed(client))
