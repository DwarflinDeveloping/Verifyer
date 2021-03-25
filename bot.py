import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())


@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name != "✅" or payload.user_id == bot.user.id:
        return
    guild = discord.utils.get(bot.guilds, id=payload.guild_id)
    import os
    if not os.path.isfile(f"data/verify_messages/{guild.id}.txt"):
        print("does not exists")
        return
    if open(f"data/verify_messages/{guild.id}.txt", "r").read() != str(payload.message_id):
        return
    user = discord.utils.get(guild.members, id=payload.user_id)
    role = discord.utils.get(guild.roles, name="verified")
    if role in user.roles:
        return
    await user.add_roles(role)
    await user.send("Welcome to our server! :)")


@bot.event
async def on_ready():
    import os
    if not os.path.isdir("data/verify_messages"):
        os.makedirs("data/verify_messages")
    print(f"Logged in as {bot.user}")


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
    elif args[0] == "get":
        verify_message_file = open(f"data/verify_messages/{ctx.guild.id}.txt", "r")
        verify_message = verify_message_file.read()
        verify_message_file.close()
        await ctx.send(f"Your guilds verify message is ```{verify_message}```")
    if len(args) != 2:
        await ctx.send("Wrong usage! See ``%verify``")
    elif args[0] == "set":
        verify_message = await ctx.channel.fetch_message(args[1])

        await verify_message.add_reaction("✅")

        verify_message_file = open(f"data/verify_messages/{ctx.guild.id}.txt", "w")
        verify_message_file.write(args[1])
        verify_message_file.close()
        await ctx.send(f"Your guilds verify message sucessfully set to ``{args[1]}``")
    else:
        await ctx.send("Wrong usage! See ``%verify``")

bot.run("TOKEN")
