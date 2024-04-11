import discord
import asyncio
import os
import random
import pyfiglet
from discord.ext import commands

sniped_messages = {}

class Verrus(commands.Cog, ):
    def __init__(self, bot):
        self.bot = bot
        print("Verrus loader (1/2) Loaded.")
    
    @commands.command(aliases=["8ball", "8b"])
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
            "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]
        await ctx.reply(f"Your question was `{question}`. And to that I say:\n{random.choice(responses)}")

    @commands.command(aliases=["+", "plus"])
    async def add(self, ctx, left: int, right: int):
        await ctx.send(left + right)

    @commands.command(aliases=["-", "subtract"])
    async def minus(self, ctx, left: int, right: int):
        await ctx.send(left - right)

    @commands.command(aliases=["×", "multip"])
    async def multiply(self, ctx, left: int, right: int):
        await ctx.send(left * right)

    @commands.command()
    async def divide(self, ctx, left: int, right: int):
        await ctx.send(left / right)

    @commands.command()
    async def ascii(self, ctx, *, text=None):
        if text is None:
            await ctx.send("You must input some text to make into Ascii!")
            return
        result = pyfiglet.figlet_format(text)
        embed = discord.Embed(description=f"```{result}```")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, *, reason=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(title="Channel locked.🔒", description=f"Reason: ```md\n{reason}```", color=0x3A56D4)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(title="Channel unlocked.🔓", color=0x3A56D4)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

    @commands.command()
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = sniped_messages[ctx.guild.id]
        except KeyError:
            await ctx.send("Couldn't find a message to snipe!")
            return
        embed = discord.Embed(description=contents, color=discord.Color.blue(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Verrus(bot))