import discord
from discord.ext import commands
import time

THRESHOLD = 2
member_list = []
time_last_join = time.time()

def antiraid(member):
    global member_list
    global time_last_join
    member_list.append(member)
    ret = False
    if time.time() - time_last_join >= 15.0:
        time_last_join = time.time()
        if len(member_list) >= THRESHOLD:
            ret = True
        member_list = []
    return ret

class ServerProtection(commands.Cog, name='Server Protection'):
    '''These are the commands used by Moderation'''
    
    def __init__(self, bot):
        self.bot = bot
        print("Server Protection Cog Loaded")
    
    async def cog_check(self, ctx):  
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return ctx.author.id == 578789460141932555
    
    @commands.Cog.listener('on_member_join')
    async def antiraid_listener(self, member):
        kick_conditional = antiraid(member)
        output_channel = self.bot.get_channel(838155702350381137) # author note, will patch and untie from spesific channel
        try:
            if kick_conditional:
                await member.kick(reason="Anti-raid")
        except Exception as E:
            pass

async def setup(bot):
    await bot.add_cog(ServerProtection(bot))