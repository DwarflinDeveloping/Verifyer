#!/usr/bin/python3

import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())
bot.help_command = None

verify_messages = []


def make_directories():
    from os.path import isdir
    if not isdir("data"):
        os.mkdir("data")
    if not isdir("data/verify_messages"):
        os.mkdir("data/verify_messages")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name != "✅" or payload.user_id == bot.user.id:
        return
    guild = discord.utils.get(bot.guilds, id=payload.guild_id)
    if payload.message_id not in verify_messages:
        return
    user = discord.utils.get(guild.members, id=payload.user_id)
    role = discord.utils.get(guild.roles, name="verified")
    if role in user.roles:
        return
    await user.add_roles(role)
    payload_channel = discord.utils.get(await guild.fetch_channels(), id=payload.channel_id)
    if discord.utils.get(await guild.fetch_channels(), id=824542556423192647) == payload_channel:
        await user.send("Welcome to our server! :slight_smile:")
    elif discord.utils.get(await guild.fetch_channels(), id=824543068379545610) == payload_channel:
        await user.send("Wilkommen auf dem Server! :slight_smile:")


@bot.event
async def on_ready():
    import os
    if not os.path.isdir("data/verify_messages"):
        os.makedirs("data/verify_messages")
    print(f"Logged in as {bot.user}")

    global verify_messages
    import json
    import os
    default_id = 822148801787199568
    if not os.path.isfile(f"data/verify_messages/{default_id}.json"):
        return
    verify_messages_file = json.loads(open(f"data/verify_messages/{default_id}.json").read()).keys()
    for verify_message in verify_messages_file:
        verify_messages += [int(verify_message)]


@bot.command()
async def verify(ctx, *args):
    if ctx.author.id != 784473264755834880:
        await ctx.send("You are not permitted to do that!")
        return
    if len(args) == 0:
        await ctx.send(
            "Usage of this command:\n"
            "``%verify get`` – outputs the verify message id\n"
            "``%verify set <message id>`` - sets the verify message\n"
        )
    elif args[0] == "get" or args[0] == "list":
        import os
        import json

        if os.path.isfile(f"data/verify_messages/{ctx.guild.id}.json"):
            verify_messages_file = json.loads(open(f"data/verify_messages/{ctx.guild.id}.json").read()).keys()
            guild_verify_messages = ""
            for verify_message in verify_messages_file:
                guild_verify_messages += f"```{verify_message}```"
            await ctx.send(f"{guild_verify_messages}")
        else:
            await ctx.send(f"This guild has no verify messages.")
    elif args[0] == "add":
        try:
            verify_message = await ctx.channel.fetch_message(args[1])
            await verify_message.add_reaction("✅")
        except:
            await ctx.send("The specified message does not exist.")
            return
        import json
        import os
        if os.path.isfile(f"data/verify_messages/{ctx.guild.id}.json"):
            with open(f"data/verify_messages/{ctx.guild.id}.json", "r") as json_file:
                verify_messages_guild = json.load(json_file)
            verify_messages_guild[args[1]] = True
            json_file.close()
        else:
            verify_messages_guild = {args[1]: True}
        with open(f"data/verify_messages/{ctx.guild.id}.json", "w") as json_file:
            json_file.write(json.dumps(verify_messages_guild, indent=4))
        json_file.close()
        global verify_messages
        verify_messages += [int(args[1])]
        await ctx.send(f"`{args[1]}` sucessfully added to the guilds verify messages.")
    elif args[0] == "clear":
        verify_message_file_path = f"data/verify_messages/{ctx.guild.id}.json"
        import os
        if os.path.isfile(verify_message_file_path):
            os.remove(verify_message_file_path)
            await ctx.send("The verify messages of this guild cleared sucessfully.")
        else:
            await ctx.send("This guild has no verify messages.")
    else:
        await ctx.send("Wrong usage! See ``%verify``")


make_directories()

bot.run(os.getenv("TOKEN"))
