import discord
from discord.ext import commands
import os
import asyncio
import json

intents = discord.Intents(value=8)
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# Syncs all bot commands, sends a message to console saying if bot is online.
@client.event
async def on_ready():
    await client.tree.sync()
    print("-------------")
    print(f"{client.user} is online.")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)


# On guild join events.
@client.event
async def on_guild_join(guild):
    with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "r") as f:
        mute_role = json.load(f)

        mute_role[str(guild.id)] = None

    # Checks if there is any one in the mute roles.
    with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "r") as f:
        mute_role = json.load(f)

        mute_role.pop(str(guild.id))

    with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)


# Loads all of the cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


# Main function that runs.
async def main():
    async with client:
        with open("/Users/zach/Documents/College/Comp Sci 1/CarnivalBot/cogs/jsonfiles/config.json", "r") as f:
            data = json.load(f)
            token = data["TOKEN"]

        await load()
        await client.start(token)


asyncio.run(main())
