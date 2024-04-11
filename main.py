from discord import app_commands, Intents, Message
from discord.ext import commands, tasks
import os
import json

intents = Intents.default()
intents.members = True
intents.message_content = True

with open("config.json", "r") as _i_config:
    config = json.load(_i_config)

def get_prefix(client, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    try:
      return prefixes[str(message.guild.id)]
    except KeyError:
        return "$"

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.owner_id = config["AUTHOR_ID"]
TOKEN = config["TOKEN"]

muted_mods = []
sniped_messages = {}

@bot.listen("on_guild_join")
async def prefix_initializer(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

    prefixes[str(guild.id)] = "$!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)

@bot.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)    

    await ctx.send(f"The prefix was changed to {prefix}")

@bot.listen('on_ready')
async def task_starter(): # I did not know how to handle this any other way... I'm sorry :C
    for filename in os.listdir('./cogs'):
        if filename == '__pycache___':
            pass
        if filename.endswith('.py'):          # Will patch next iteration or when I figure out a better method
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.listen('on_message')
async def check_for_pings(msg : Message):
    guild_id = msg.guild.id
    if msg.content == "<@" + str(bot.user.id) + ">":
        with open("prefixes.json", "r") as unloaded_prefixes:
            loaded_prefixes = json.load(unloaded_prefixes)
        try:
            return await msg.channel.send(f"My prefix for this server is `{loaded_prefixes[guild_id]}`")
        except KeyError:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
                prefixes[str(msg.guild.id)] = "!"

        with open("prefixes.json", "w") as f:
            json.dump(prefixes,f)
            f.close()
            loaded_prefixes.close()
            return await msg.send("My prefix for this server is `!`")
        
bot.run(TOKEN)