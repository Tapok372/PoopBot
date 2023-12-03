import disnake
import random

from disnake.ext import commands
from utils import user

class fun(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    @commands.slash_command(name = 'sex', description = 'Команда для жосткого секса')
    async def sex(self, inter, user: disnake.User = commands.Param(name = 'игрок', description = 'Выбери того, с кем хочешь секс')):
        embed = disnake.Embed(description = f'{inter.author.mention} **трахнул(а)** {user.mention}',colour = 3092790)
        embed.set_image(url = 'https://cdn.discordapp.com/attachments/1004371026131562507/1082708159325540473/IMG_0245.gif')
        await inter.response.send_message(f"{user.mention}", embed = embed)
    
    @commands.slash_command(name = 'me', description = 'Команда для отыгрыша действия')
    async def me(self, inter, description: str = commands.Param(name = 'действие', description = 'Введите действие которое хотите отыграть')):
        nickname = user.User.nickname_check(member = inter.author)
        await inter.response.send_message(f'**{nickname}** {description}.')
    
    @commands.slash_command(name = 'try', description = 'Попытаться сделать действие')
    async def tryes(self, inter, description : str = commands.Param(name = 'действие', description = 'Введите действие которое хотите отыграть')):
        nickname = user.User.nickname_check(member = inter.author)
        tryes = ['Удачно', 'Неудачно', 'Успех', 'Провал']
        await inter.response.send_message(f'**{nickname}** {description} `{random.choice(tryes)}`.')
        
def setup(bot):
    bot.add_cog(fun(bot))