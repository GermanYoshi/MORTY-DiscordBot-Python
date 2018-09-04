from discord.ext import commands
import discord
import asyncio
from funktionen import error_embed

bot = commands.Bot(command_prefix="!", case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='!help'))
    print("###########################")
    print("Logged in Successfully")
    print("Ready to Rumble!")
    print("###########################")
    print("Running on:")
    print(f"{len(bot.servers)} servers")
    print("###########################")


@bot.event
async def on_member_update(before, after):
    if before == bot.user and after.display_name != "MORTY":
        await bot.change_nickname(after, nickname=None)


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return await bot.send_message(ctx.message.channel, embed=await error_embed(f":x: The command **{ctx.invoked_with}** does not exist!"))
    if isinstance(error, commands.CommandInvokeError):
        is_forbidden = isinstance(error.original, discord.Forbidden)
        if is_forbidden:
            return await bot.send_message(ctx.message.channel, embed=await error_embed(f":x: You do not have permission to use **{ctx.invoked_with}**! / do !permissions"))


@bot.command()
async def serverlist():
    em = discord.Embed(color=discord.Color.green(), description=f"Running on **{len(bot.servers)}** Server(s)")
    await bot.say(embed=em)


@bot.command()
async def ping():
    em = discord.Embed(color=discord.Color.green(), description="**Pong!**")
    await bot.say(embed=em)


@bot.command()
async def invite():
    link = "https://discordapp.com/oauth2/authorize?&client_id=476379664450060289&scope=bot&permissions=8"
    em = discord.Embed(color=discord.Color.green(),
                       description=f"Click [**HERE**]({link}) to Invite the Bot to your Server!")
    await bot.say(embed=em)


@bot.command()
async def support():
    link = "https://discord.gg/CCFsKk"
    em = discord.Embed(color=discord.Color.green(), description=f"Click [**HERE**]({link}) to join our Support Server!")
    await bot.say(embed=em)


@bot.command()
async def help():
    em = discord.Embed(color=discord.Color.orange())
    em.add_field(name="**!help**", value="Shows a list of all available Commands!", inline=False)
    em.add_field(name="**!permissions**", value="Shows a list for all Mod commands needed permissions!", inline=False)
    em.add_field(name="**!ping**", value="Pings the Bot!", inline=False)
    em.add_field(name="**!mirror [Name]**", value="Look in the mirror!", inline=False)
    em.add_field(name="**!invite**", value="Invite the Bot to your Server!", inline=False)
    await bot.say(embed=em)


@bot.command()
async def permissions():
    em = discord.Embed(color=discord.Color.dark_blue())
    em.add_field(name="**!warn**", value="Needs the **Support Team** Rank!", inline=False)
    em.add_field(name="**!clear**", value="Needs the **Staff** Rank!", inline=False)
    em.add_field(name="**!mute**", value="Needs the **Staff** Rank!", inline=False)
    em.add_field(name="**!kick**", value="Needs the **Staff** Rank!", inline=False)
    em.add_field(name="**!ban**", value="Needs the **Admin** Rank!", inline=False)
    em.add_field(name="**!support**", value="**Get the Link to the Support Server!**", inline=False)
    await bot.say(embed=em)


@bot.command(pass_context=True, name="mirror")
async def mirror_(ctx, *, user: discord.Member = None):
    em = discord.Embed(color=discord.Color.green())
    em.set_image(url=user.avatar_url if user else ctx.message.author.avatar_url)
    return await bot.say(embed=em)


@bot.command(pass_context=True)
@commands.has_role("Support Team")
async def warn(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Warned!",
                          description="**{0}** was warned by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
@commands.has_role("Staff")
async def clear(ctx, num: int = 100):
    deleted = await bot.purge_from(ctx.message.channel, limit=num)
    em = discord.Embed(color=discord.Color.dark_blue(), description=f"✅ Deleted {len(deleted)} message(s)")
    await bot.say(embed=em)
    await asyncio.sleep(2)
    await bot.purge_from(ctx.message.channel, limit=1)


@bot.command(pass_context=True)
@commands.has_role("Staff")
async def c(ctx, num: int = 100):
    deleted = await bot.purge_from(ctx.message.channel, limit=num)
    em = discord.Embed(color=discord.Color.dark_blue(), description=f"✅ Deleted {len(deleted)} message(s)")
    await bot.say(embed=em)
    await asyncio.sleep(2)
    await bot.purge_from(ctx.message.channel, limit=1)


@bot.command(pass_context=True)
@commands.has_role("Staff")
async def mute(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    role = discord.utils.get(member.server.roles, name='Muted')
    await bot.add_roles(member, role)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Muted!",
                          description="**{0}** was muted by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
@commands.has_role("Staff")
async def kick(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    await bot.kick(member)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Kicked!",
                          description="**{0}** was kicked by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
@commands.has_role("Admin")
async def ban(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    await bot.ban(member)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Banned!",
                          description="**{0}** was banned by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


bot.run("NDg2MTY5NzkyODEwODQ0MTcw.Dm7MuQ.VME-GG2hBCfOgeq-RCychQkspoc")
