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
async def on_command(cmd, ctx):
    print(cmd, ctx)


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return await bot.send_message(ctx.message.channel, embed=await error_embed(f":x: The command **{ctx.invoked_with}** does not exist!"))
    if isinstance(error, commands.CommandInvokeError):
        is_forbidden = isinstance(error.original, discord.Forbidden)
        if is_forbidden:
            return await bot.send_message(ctx.message.channel, embed=await error_embed(f":x: You do not have permission to use **{ctx.invoked_with}**! / do !permissions"))
    if isinstance(error, commands.MissingRequiredArgument):
        return await bot.send_message(ctx.message.channel, embed=await error_embed(f":x: The command **{ctx.invoked_with}** need a argument!"))
    if isinstance(error, commands.BadArgument):
        return await bot.send_message(ctx.message.channel, embed=await error_embed(f":x: unknown argument **{ctx.invoked_with}** !"))
    if isinstance(error, commands.CommandError):
        return await bot.send_message(ctx.message.channel, embed=await error_embed(":x: An error occurred!"))
    if isinstance(error, commands.CommandInvokeError):
        return await bot.send_message(ctx.message.channel, embed=await error_embed(":x: An error occurred!"))
    if isinstance(error, commands.CommandOnCooldown):
        return await bot.send_message(ctx.message.channel, embed=await error_embed(":x: You`re to fast!"))


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def status():
    em = discord.Embed(color=discord.Color.green(), description=f"Running on **{len(bot.servers)}** Server(s)")
    await bot.say(embed=em)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping():
    em = discord.Embed(color=discord.Color.green(), description="**Pong!**")
    await bot.say(embed=em)


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def invite():
    link = "https://discordapp.com/oauth2/authorize?&client_id=476379664450060289&scope=bot&permissions=8"
    em = discord.Embed(color=discord.Color.green(),
                       description=f"Click [**HERE**]({link}) to Invite the Bot to your Server!")
    await bot.say(embed=em)


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def support():
    link = "https://discord.gg/CCFsKk"
    em = discord.Embed(color=discord.Color.green(), description=f"Click [**HERE**]({link}) to join our Support Server!")
    await bot.say(embed=em)


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def donate():
    link = "https://www.paypal.me/OfficialMortyBot"
    em = discord.Embed(color=discord.Color.green(), description=f"Click [**HERE**]({link}) to donate!")
    await bot.say(embed=em)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.channel)
async def help():
    em = discord.Embed(color=discord.Color.orange())
    em.add_field(name="**!help**", value="Shows a list of all available Commands!", inline=False)
    em.add_field(name="**!permissions**", value="Shows a list for all Mod commands needed permissions!", inline=False)
    em.add_field(name="**!status**", value="Show the status of the bot!", inline=False)
    em.add_field(name="**!ping**", value="Pings the Bot!", inline=False)
    em.add_field(name="**!mirror [Name]**", value="Look in the mirror!", inline=False)
    em.add_field(name="**!invite**", value="Invite the Bot to your Server!", inline=False)
    em.add_field(name="**!warn**", value="Warn a Player!", inline=False)
    em.add_field(name="**!clear [amount]**", value="Clear the chat!", inline=False)
    em.add_field(name="**!mute**", value="Mute a Player!", inline=False)
    em.add_field(name="**!kick**", value="Kick a Player!", inline=False)
    em.add_field(name="**!ban**", value="Ban a Player!", inline=False)
    em.add_field(name="**!support**", value="**Get the Link to the Support Server!**", inline=False)
    em.add_field(name="**!donate**", value="**Donate to support the bot**", inline=False)
    await bot.say(embed=em)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.channel)
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
@commands.cooldown(1, 5, commands.BucketType.user)
async def mirror_(ctx, *, user: discord.Member = None):
    em = discord.Embed(color=discord.Color.green())
    em.set_image(url=user.avatar_url if user else ctx.message.author.avatar_url)
    return await bot.say(embed=em)


@bot.command(pass_context=True)
@commands.has_role("Support Team")
@commands.cooldown(1, 2, commands.BucketType.user)
async def warn(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Warned!",
                          description="**{0}** was warned by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
@commands.has_role("Staff")
@commands.cooldown(1, 5, commands.BucketType.channel)
async def clear(ctx, num: int = 100):
    deleted = await bot.purge_from(ctx.message.channel, limit=num)
    em = discord.Embed(color=discord.Color.dark_blue(), description=f"✅ Deleted {len(deleted)} message(s)")
    await bot.say(embed=em)
    await asyncio.sleep(2)
    await bot.purge_from(ctx.message.channel, limit=1)


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
@commands.has_role("Staff")
async def c(ctx, num: int = 100):
    deleted = await bot.purge_from(ctx.message.channel, limit=num)
    em = discord.Embed(color=discord.Color.dark_blue(), description=f"✅ Deleted {len(deleted)} message(s)")
    await bot.say(embed=em)
    await asyncio.sleep(2)
    await bot.purge_from(ctx.message.channel, limit=1)


@bot.command(pass_context=True)
@commands.has_role("Staff")
@commands.cooldown(1, 2, commands.BucketType.user)
async def mute(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    role = discord.utils.get(member.server.roles, name='Muted')
    await bot.add_roles(member, role)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Muted!",
                          description="**{0}** was muted by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
@commands.has_role("Staff")
@commands.cooldown(1, 2, commands.BucketType.user)
async def unmute(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    role = discord.utils.get(member.server.roles, name='Muted')
    await bot.remove_roles(member, role)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User unmuted!",
                          description="**{0}** was unmuted by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
@commands.has_role("Staff")
@commands.cooldown(1, 2, commands.BucketType.user)
async def kick(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    await bot.kick(member)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Kicked!",
                          description="**{0}** was kicked by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
@commands.has_role("Admin")
@commands.cooldown(1, 2, commands.BucketType.user)
async def ban(ctx, member: discord.Member):
    await bot.purge_from(ctx.message.channel, limit=1)
    await bot.ban(member)
    embed = discord.Embed(color=discord.Color.dark_blue(), title="User Banned!",
                          description="**{0}** was banned by **{1}**!".format(member, ctx.message.author))
    await bot.say(embed=embed)


bot.run("NDg2MTY5NzkyODEwODQ0MTcw.DnXs3Q.FZx25GrWDsW1AAbbsgM9B_O_kZM")
