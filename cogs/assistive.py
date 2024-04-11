import discord
from discord.ext import commands
from PersonalUtils import dbms

# db = dbms.Database(db_path="mod_files.json", cache=True)

class AssistiveCommands(commands.Cog, name='Assistive Commands'):
    '''These are the commands used to assist activities making them easier'''
    
    def __init__(self, bot):
        self.bot = bot
        print("Assistive Cog Loaded")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, reason=None):
        if reason is None:
            reason = f"Member kicked by {ctx.author.id}"
        await member.kick(reason)
        await ctx.reply(f"Done!, {member.id} has been kicked.", mention_author=False)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason)
        if reason is None:
            reason = f"Member banned by {ctx.author.id}"
        await ctx.reply(f"Done!, {member.id} has been banned.", mention_author=False)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member : discord.Member, *, reason : str =None):
        if reason is None:
            reason = f"Member unbanned by {ctx.author.id}"
        await member.unban(reason)
        await ctx.reply(f"Done!, {member.id} has been unbanned.", mention_author=False)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def hide_channel(self, ctx, channel=None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        try:
            await ctx.reply(f"Channel <#{channel.id}> has been hidden from `@everyone`", mention_author=False)
        except Exception:
            pass
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unhide_channel(self, ctx, channel=None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        try:
            await ctx.reply(f"Channel <#{channel.id}> has been hidden from `@everyone`", mention_author=False)
        except Exception:
            pass

async def setup(bot):
    await bot.add_cog(AssistiveCommands(bot))