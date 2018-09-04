import discord


async def error_embed(text):
    return discord.Embed(description=text, color=discord.Color.red())
