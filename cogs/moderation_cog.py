import discord
from discord.ext import commands
from PersonalUtils import dbms

db = dbms.Database(db_path="mod_files.json", cache=True)

with open("banned_nicknames.txt", "r") as _banned_list:
    banned_list = _banned_list.readlines()

class ModerationCommands(commands.Cog, name='Moderation Commands'):
    '''These are the commands used by Moderation'''
    
    def __init__(self, bot):
        self.bot = bot
        print("Moderation Cog Loaded")  
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shh(self, ctx, mutee : discord.Member):
        db.write(str(mutee.id), True)
        await ctx.reply(f"`{mutee.id}` has been shh'd.", mention_author=False)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unshh(self, ctx, mutee : discord.Member):
        db.write(str(mutee.id), False)
        await ctx.reply(f"`{mutee.id}` has been unshh'd.", mention_author=False)

    @commands.Cog.listener('on_message')
    async def listen_for_shh(self, msg):
        try:
            if db.read()[str(msg.author.id)]:
                await msg.delete()
        except KeyError:
            return None
        
    @commands.Cog.listener('on_member_update')
    async def nickname_moderator(self, before : discord.Member, after: discord.Member):
        banned_nicknames = banned_list
        after_nick = after.nick
        if after_nick:
            if after_nick.lower() in banned_nicknames:
                last_nickname = before.nick
                if last_nickname:
                    await after.edit(nick=last_nickname)
                else:
                    await after.edit(nick="[Moderated]")
        

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))