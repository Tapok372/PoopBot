import disnake
from disnake.ext import commands
from disnake import ButtonStyle
import asyncio
import disnake

class RR(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_any_role(995739756581355601)
    async def r(self, ctx):
        guild = self.bot.get_guild(995379037407027270)
        roleCity = guild.get_role(1001919800546701443)
        roleEvent = guild.get_role(1001919876216131654)
        roleCenitel = guild.get_role(1016410597648253048)
        rolePhoto = guild.get_role(1070029677936255027)
        roleVolont = guild.get_role(1079062065567760535)
        roleZril = guild.get_role(1144315643227803889)
        roleV1 = guild.get_role(1036335715287580792)
        roleV2 = guild.get_role(1036336023598284800)
        roleV3 = guild.get_role(1036335703832932525)
        roleV4 = guild.get_role(1036335919306915872)

        row_of_buttons = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "🔔",
                label = (len(roleCity.members)),
                custom_id = "rr1"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "🎮",
                label = (len(roleEvent.members)),
                custom_id = "rr2"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "🎨",
                label = (len(roleCenitel.members)),
                custom_id = "rr3"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "📷",
                label = (len(rolePhoto.members)),
                custom_id = "rr4"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "📦",
                label = (len(roleVolont.members)),
                custom_id = "rr5"
            ) 
        )
        row_of_buttons2 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "📹",
                label = (len(roleZril.members)),
                custom_id = "rr6"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Red:1036337369009360956>",
                label = (len(roleV1.members)),
                custom_id = "rv1"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Green:1036337365909766284>",
                label = (len(roleV2.members)),
                custom_id = "rv2"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Blue:1036337369911132254>",
                label = (len(roleV3.members)),
                custom_id = "rv3"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Yellow:1036337367369400331>",
                label = (len(roleV4.members)),
                custom_id = "rv4"
            )
        )
        
        
        

        embed = disnake.Embed(title = ':information_source: Получение ролей :information_source:', description = """Чтобы получить роль нажмите на кнопку.

> **📝Количество обладателей ролей:**

**🔔 - Ищу город** - Роль для тех, кто хочет найти себе город.  

**🎮 - Ивенты** - Роль для получения уведомлений о предстоящих ивентах 

**🎨 - Ценитель** - Роль для ценителей артов

**📷 - Фотокарточки** - Роль для получения уведмолений о новых фотокарточках в канале <#995744289520877578>

**📦 - Волонтёр** - Роль для волонтёров, которые могут получить задание от глав организаций в канале <#1079053216718799020>

**📹 - Любитель Посмотреть** - Роль для контент-мейкеров. Используется при пинге заинтересованных игроков о стриме или видео по PoopLand'у в канале <#1049081667131801600>                               

> **Роли веток:**

**<:Red:1036337369009360956> - Красная ветка** 
**<:Green:1036337365909766284> - Зелёная ветка** 
**<:Blue:1036337369911132254> - Голубая ветка** 
**<:Yellow:1036337367369400331> - Жёлтая ветка**""", colour = 3092790)
        await ctx.send(embed = embed, components = [row_of_buttons, row_of_buttons2])
        
        
    @commands.slash_command(name = 'бустер', description = 'Команда для бустеров сервера')
    @commands.has_any_role(996818993962831873, 995739756581355601)
    async def boost(self, inter):
        row1 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '<:967DDD:1036333014759768074>',
                custom_id = 'colour1'
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '<:7EE65B:1036333012981387334>',
                custom_id = 'colour2'
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '<:5B9BE6:1036333010980720792>',
                custom_id = 'colour3'
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '<:E7AF28:1036333009978282095>',
                custom_id = 'colour4'
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '<:FA8072:1036333008438972607>',
                custom_id = 'colour5'
            ),
        )
        row2 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '<:s_:1041323937029697556>',
                custom_id = 'colour6'
            )
        )
        emb = disnake.Embed(title = 'Нажми на кнопку с нужным цветом', colour = 3092790)
        await inter.send(embed = emb, components = [row1, row2], ephemeral = True)


    @commands.slash_command(name = 'роли-спавн', guild_ids = [1004458000116891798], description = 'Вызывает панель выдачи ролей')
    @commands.has_permissions(administrator = True)
    async def roles_spawn(self, inter):
        embed = disnake.Embed(title = 'Получение ролей', description = """**Чтобы получить роль - нажмите на кнопку**

🎨 **Строитель**

👷 **Перестройщик**

🔨 **Ресурсер**""", colour = 3092790)
        row1 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '🎨',
                custom_id = 'Строитель'
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '👷',
                custom_id = 'Перестройщик'
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = '🔨',
                custom_id = 'Ресурсер'
            )
        )
        await inter.send(embed = embed, components = [row1])
    
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        ##Роли канала "Получение ролей"
        guild = self.bot.get_guild(995379037407027270)
        roleCity = guild.get_role(1001919800546701443)
        roleEvent = guild.get_role(1001919876216131654)
        roleCenitel = guild.get_role(1016410597648253048)
        rolePhoto = guild.get_role(1070029677936255027)
        roleVolont = guild.get_role(1079062065567760535)
        roleZril = guild.get_role(1144315643227803889)
        roleV1 = guild.get_role(1036335715287580792)
        roleV2 = guild.get_role(1036336023598284800)
        roleV3 = guild.get_role(1036335703832932525)
        roleV4 = guild.get_role(1036335919306915872)


        #Буст цвета
        roleCol1 = guild.get_role(1036328772053499994)
        roleCol2 = guild.get_role(1036328534727196712)
        roleCol3 = guild.get_role(1036328094946054155)
        roleCol4 = guild.get_role(1036327805115453511)
        roleCol5 = guild.get_role(1036327408594325735)
        roleCol6 = guild.get_role(1041321228432052224)


        #Роли ДС спавна
        spawn_guild = guild = self.bot.get_guild(1004458000116891798) 
        roleBuilder = spawn_guild.get_role(1004662418531696781)
        roleReBuilder = spawn_guild.get_role(1004662457492570192)
        roleResourc = spawn_guild.get_role(1004662575646117961)
        roleRab = spawn_guild.get_role(1004662238306631700)
        roleIsp = spawn_guild.get_role(1006646478082682940)

        row_of_buttons = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "🔔",
                label = (len(roleCity.members)),
                custom_id = "rr1"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "🎮",
                label = (len(roleEvent.members)),
                custom_id = "rr2"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "🎨",
                label = (len(roleCenitel.members)),
                custom_id = "rr3"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "📷",
                label = (len(rolePhoto.members)),
                custom_id = "rr4"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "📦",
                label = (len(roleVolont.members)),
                custom_id = "rr5"
            )
            

            
        )
        row_of_buttons2 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "📹",
                label = (len(roleZril.members)),
                custom_id = "rr6"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Red:1036337369009360956>",
                label = (len(roleV1.members)),
                custom_id = "rv1"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Green:1036337365909766284>",
                label = (len(roleV2.members)),
                custom_id = "rv2"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Blue:1036337369911132254>",
                label = (len(roleV3.members)),
                custom_id = "rv3"
            ),
            disnake.ui.Button(
                style = ButtonStyle.green,
                emoji = "<:Yellow:1036337367369400331>",
                label = (len(roleV4.members)),
                custom_id = "rv4"
            )
        )
        
        
        
        
        

        member = inter.author
        if inter.channel.id == 1001920807414538311:
            await inter.send('Роль обновлена', ephemeral = True)

        if inter.component.custom_id == "rv1":
            if roleV1 in inter.author.roles:
                await member.remove_roles(roleV1)
            else:
                await member.add_roles(roleV1)
                await member.remove_roles(roleV2, roleV3, roleV4)

        if inter.component.custom_id == "rv2":
            if roleV2 in inter.author.roles:
                await member.remove_roles(roleV2)
            else:
                await member.add_roles(roleV2)
                await member.remove_roles(roleV1, roleV3, roleV4)

        if inter.component.custom_id == "rv3":
            if roleV3 in inter.author.roles:
                await member.remove_roles(roleV3)
            else:
                await member.add_roles(roleV3)
                await member.remove_roles(roleV1, roleV2, roleV4)

        if inter.component.custom_id == "rv4":
            if roleV4 in inter.author.roles:
                await member.remove_roles(roleV4)
            else:
                await member.add_roles(roleV4)
                await member.remove_roles(roleV1, roleV2, roleV3)


        if inter.component.custom_id == "colour1":
            if roleCol1 in inter.author.roles:
                await member.remove_roles(roleCol1)
            else:
                await member.add_roles(roleCol1)
                await member.remove_roles(roleCol2, roleCol3, roleCol4, roleCol5, roleCol6)
                await inter.response.send_message(f'Роль {roleCol1.name} обновлена', ephemeral = True)
        
        if inter.component.custom_id == "colour2":
            if roleCol2 in inter.author.roles:
                await member.remove_roles(roleCol2)
            else:
                await member.add_roles(roleCol2)
                await member.remove_roles(roleCol1, roleCol3, roleCol4, roleCol5, roleCol6)
                await inter.response.send_message(f'Роль {roleCol2.name} обновлена', ephemeral = True)
        
        if inter.component.custom_id == "colour3":
            if roleCol3 in inter.author.roles:
                await member.remove_roles(roleCol3)
            else:
                await member.add_roles(roleCol3)
                await member.remove_roles(roleCol1, roleCol2, roleCol4, roleCol5, roleCol6)
                await inter.response.send_message(f'Роль {roleCol3.name} обновлена', ephemeral = True)
            
        if inter.component.custom_id == "colour4":
            if roleCol4 in inter.author.roles:
                await member.remove_roles(roleCol4)
            else:
                await member.add_roles(roleCol4)
                await member.remove_roles(roleCol1, roleCol2, roleCol3, roleCol5, roleCol6)
                await inter.response.send_message(f'Роль {roleCol4.name} обновлена', ephemeral = True)
        
        if inter.component.custom_id == "colour5":
            if roleCol5 in inter.author.roles:
                await member.remove_roles(roleCol5)
            else:
                await member.add_roles(roleCol5)
                await member.remove_roles(roleCol1, roleCol2, roleCol3, roleCol4, roleCol6)
                await inter.response.send_message(f'Роль {roleCol5.name} обновлена', ephemeral = True)
            
        if inter.component.custom_id == "colour6":
            if roleCol6 in inter.author.roles:
                await member.remove_roles(roleCol6)
            else:
                await member.add_roles(roleCol6)
                await member.remove_roles(roleCol1, roleCol2, roleCol3, roleCol4, roleCol5)
                await inter.response.send_message(f'Роль {roleCol6.name} обновлена', ephemeral = True)

                
        if inter.component.custom_id == "rr1":
            if roleCity in inter.author.roles:
                await member.remove_roles(roleCity)
            else:
                await member.add_roles(roleCity)
        
        if inter.component.custom_id == "rr2":
            if roleEvent in inter.author.roles:
                await member.remove_roles(roleEvent)
            else:
                await member.add_roles(roleEvent)
        
        if inter.component.custom_id == "rr3":
            if roleCenitel in inter.author.roles:
                await member.remove_roles(roleCenitel)
            else:
                await member.add_roles(roleCenitel)
        
        if inter.component.custom_id == "rr4":
            if rolePhoto in inter.author.roles:
                await member.remove_roles(rolePhoto)
            else:
                await member.add_roles(rolePhoto)
        
        if inter.component.custom_id == "rr5":
            if roleVolont in inter.author.roles:
                await member.remove_roles(roleVolont)
            else:
                await member.add_roles(roleVolont)

        if inter.component.custom_id == "rr6":
            if roleZril in inter.author.roles:
                await member.remove_roles(roleZril)
            else:
                await member.add_roles(roleZril)
        
        if inter.channel.id == 1148251647194185748:
            if roleRab in inter.author.roles or roleIsp in inter.author.roles:
                await inter.send(f'Роль {inter.component.custom_id} обновлена', ephemeral = True)
                if inter.component.custom_id == "Строитель": 
                    if roleBuilder in inter.author.roles:
                        await member.remove_roles(roleBuilder)
                    else:
                        await member.add_roles(roleBuilder)

                elif inter.component.custom_id == "Перестройщик":
                    if roleReBuilder in inter.author.roles:
                        await member.remove_roles(roleReBuilder)
                    else:
                        await member.add_roles(roleReBuilder)

                elif inter.component.custom_id == "Ресурсер":
                    if roleResourc in inter.author.roles:
                        await member.remove_roles(roleResourc)
                    else:
                        await member.add_roles(roleResourc)
            else:
                await inter.send('Вы не являетесь работником Спавна', ephemeral = True)

        channel = await self.bot.fetch_channel(1001920807414538311)
        msg = await channel.fetch_message(1070034056315678730)
        embed = disnake.Embed(title = ':information_source: Получение ролей :information_source:', description = """Чтобы получить роль нажмите на кнопку.

> **📝Количество обладателей ролей:**

**🔔 - Ищу город** - Роль для тех, кто хочет найти себе город.  

**🎮 - Ивенты** - Роль для получения уведомлений о предстоящих ивентах 

**🎨 - Ценитель** - Роль для ценителей артов

**📷 - Фотокарточки** - Роль для получения уведмолений о новых фотокарточках в канале <#995744289520877578>

**📦 - Волонтёр** - Роль для волонтёров, которые могут получить задание от глав организаций в канале <#1079053216718799020>

**📹 - Любитель Посмотреть** - Роль для контент-мейкеров. Используется при пинге заинтересованных игроков о стриме или видео по PoopLand'у в канале <#1049081667131801600>                               

> **Роли веток:**

**<:Red:1036337369009360956> - Красная ветка** 
**<:Green:1036337365909766284> - Зелёная ветка** 
**<:Blue:1036337369911132254> - Голубая ветка** 
**<:Yellow:1036337367369400331> - Жёлтая ветка**""", colour = 3092790)
        await msg.edit(embed = embed, components = [row_of_buttons, row_of_buttons2])

    
    
    
    
    
    
    
    
    
    

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog RR ready!")
    
def setup(bot):
    bot.add_cog(RR(bot))
