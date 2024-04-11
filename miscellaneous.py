import discord
from discord.ext import commands
from PersonalUtils import dbms

db = dbms.Database(db_path="mod_files.json", cache=True)

class ModerationCommands(commands.Cog, name='gyat damn funny shi Commands'):
    '''These are the commands used by Moderation'''
    
    def __init__(self, bot):
        self.bot = bot
        print("Moderation Cog Loaded ")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shh(self, ctx, mutee : discord.Member):
        db.write(str(mutee.id), True)
        await ctx.reply(f"`{mutee.id}` has been shh'd.")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unshh(self, ctx, mutee : discord.Member):
        db.write(str(mutee.id), False)
        await ctx.reply(f"`{mutee.id}` has been unshh'd.")

    @commands.Cog.listener('on_message')
    async def listen_for_shh(self, msg):
        if db.read(pass_through=True)[msg.author.id]:
            return await msg.delete()
        

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))