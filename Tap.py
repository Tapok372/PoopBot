import disnake
from disnake.ext import commands 
import os
import datetime

intents = disnake.Intents().all()

bot = commands.Bot(
    command_prefix = "!",
    intents=intents
)
bot.remove_command("help")



@bot.event
async def on_ready():
    print("Poop Bot started")
    


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Cogs is reloaded...")
    await ctx.message.delete()



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
    
    
bot.run('ТОКЕН')

