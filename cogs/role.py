import dataclasses
import disnake
from disnake.ext import commands
from disnake.utils import get

class SRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description = 'Commands remove message')
    @commands.has_any_role(995739756581355601)
    async def purg(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        limit: int,
        member: disnake.Member =None,
    ):
        msg = []
        try:
            limit = int(limit)
        except:
            return await interaction.response.send_message("Введите количество сообщений для удаления", ephemeral = True)
        if not member:
            await interaction.channel.purge(limit=limit)
            return await interaction.response.send_message(f"Очищено {limit} сообщений", ephemeral = True)
        async for m in interaction.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await interaction.response.send_message(f"Очищено {limit} сообщений {member.mention}", ephemeral = True)
    
    @commands.slash_command(description = 'Техническая команда МЗ')
    @commands.has_any_role(1006931686644269176, 995739756581355601)
    async def мз(self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        stat: str = commands.Param(choices=["Принять", "Уволить"]),
    ):
        roleE = disnake.utils.get(inter.guild.roles,id = 1006932328502800434)
        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if stat == "Принять":
            await user.add_roles(roleE)
        else:
            await user.remove_roles(roleE)

    @commands.slash_command(description = 'Техническая команда ПД')
    @commands.has_any_role(995739756581355601, 995744116866564146,995742973897740429)
    async def пд(self, 
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        role: str = commands.Param(choices={"Сотрудник ПД" : "Сотрудник ПД", "Детектив" : "Детектив"}),
        stat: str = commands.Param(choices=["Принять", "Уволить"]),
    ):
        roleS = disnake.utils.get(inter.guild.roles,id = 995743116118204506)
        roleD = disnake.utils.get(inter.guild.roles,id = 995744050143580161)

        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if role == "Сотрудник ПД":
            if stat == "Принять":
                await user.add_roles(roleS)
            else:
                await user.remove_roles(roleS)
        else:
            if stat == "Принять":
                await user.add_roles(roleD)
            else:
                await user.remove_roles(roleD)
        
    @commands.slash_command(description = 'Техническая команда Паспортного стола')
    @commands.has_any_role(995739756581355601,1012468423076360273)
    async def паспортист(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        role: str = commands.Param(choices={"passportist" : "passportist", "notariys" : "notariys"}),
        stat: str = commands.Param(choices=["Принять", "Уволить"])
    ):
        roleE = disnake.utils.get(inter.guild.roles,id = 1023278766518194249)
        roleN = disnake.utils.get(inter.guild.roles,id = 1174743838804426822)
        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if role == "passportist":
            if stat == "Принять":
                await user.add_roles(roleE)
            else:
                await user.remove_roles(roleE)
        if role == "notariys":
            if stat == "Принять":
                await user.add_roles(roleN)
            else:
                await user.remove_roles(roleN)

    @commands.slash_command(description = 'Техническая команда Министерство Юстиции ')
    @commands.has_any_role(995739756581355601,1012468423076360273)
    async def мэр(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        stat: str = commands.Param(choices=["Принять", "Уволить"])
    ):
        roleE = disnake.utils.get(inter.guild.roles,id = 1115020056531828898)
        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if stat == "Принять":
            await user.add_roles(roleE)
        else:
            await user.remove_roles(roleE) 
    
    @commands.slash_command(description = 'Техническая команда Банка')
    @commands.has_any_role(995739756581355601,1027983535308542043, 995742798554869830)
    async def банкир(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        stat: str = commands.Param(choices=["Принять", "Уволить"])
    ):
        roleE = disnake.utils.get(inter.guild.roles,id = 995743178965651456)
        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if stat == "Принять":
            await user.add_roles(roleE)
        else:
            await user.remove_roles(roleE)

    @commands.slash_command(description = 'Техническая команда МК')
    @commands.has_any_role(995739756581355601,1048894734476775515)
    async def мк(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        stat: str = commands.Param(choices=["Принять", "Уволить"])
    ):
        roleE = disnake.utils.get(inter.guild.roles,id = 1025871486013161502)
        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if stat == "Принять":
            await user.add_roles(roleE)
        else:
            await user.remove_roles(roleE)
    
    @commands.slash_command(description = 'Техническая команда МЗ')
    @commands.has_any_role(995739756581355601,1006931686644269176)
    async def мз(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        stat: str = commands.Param(choices=["Принять", "Уволить"])
    ):
        roleE = disnake.utils.get(inter.guild.roles,id = 1006932328502800434)
        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if stat == "Принять":
            await user.add_roles(roleE)
        else:
            await user.remove_roles(roleE)
    
    @commands.slash_command(description = 'Техническая команда Судейство')
    @commands.has_any_role(995739756581355601,995744116866564146)
    async def судейство(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        role: str = commands.Param(choices={"Судья" : "Судья", "Писарь" : "Писарь", "Прокурор" : "Прокурор", "Адвокат" : "Адвокат"}),
        stat: str = commands.Param(choices=["Принять", "Уволить"])
    ):
        roleSotr = disnake.utils.get(inter.guild.roles,id = 1007619059682119721)
        roleSyd = disnake.utils.get(inter.guild.roles,id = 995744230888701983)
        rolePis = disnake.utils.get(inter.guild.roles,id = 1004477825279066203)
        rolePro = disnake.utils.get(inter.guild.roles,id = 1014499600859660379)
        roleAdv = disnake.utils.get(inter.guild.roles,id = 1016719349156954113)
        await inter.response.send_message(content = f'Роль {user.name} обновлена', ephemeral = True)
        if role == "Судья":
            if stat == "Принять":
                await user.add_roles(roleSyd, roleSotr)
            else:
                await user.remove_roles(roleSyd, roleSotr)
        if role == "Писарь":
            if stat == "Принять":
                await user.add_roles(rolePis, roleSotr)
            else:
                await user.remove_roles(rolePis, roleSotr)
        if role == "Прокурор":
            if stat == "Принять":
                await user.add_roles(rolePro)
            else:
                await user.remove_roles(rolePro)
        if role == "Адвокат":
            if stat == "Принять":
                await user.add_roles(roleAdv)
            else:
                await user.remove_roles(roleAdv)

        
def setup(bot):
    bot.add_cog(SRole(bot))    
