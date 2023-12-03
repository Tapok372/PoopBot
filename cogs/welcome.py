import disnake
from disnake.ext import commands
from disnake import Localized, ButtonStyle
import sqlite3

class Welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль welcome загружен!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild1 = self.bot.get_guild(1073259328213106689)
    
        if member.guild == guild1:
            role = self.bot.get_role(1073260475757891657)
            await member.add_roles(role)
        guild = self.bot.get_guild(995379037407027270)
        if member.guild == guild:
            channel = guild.get_channel(1067468355461730384)
            avatar_url = member.avatar
            if avatar_url == None:
                avatar_url = 'https://media.discordapp.net/attachments/982269337727549530/982275492096901130/123123.png'
            embed = disnake.Embed(title = f'{member.name} присоеденился к нам!', colour = 3908957)
            embed.set_thumbnail(url = avatar_url)
            await channel.send(f'{member.mention}',embed = embed)

            DMembed = disnake.Embed(title = 'Приветсвую в дискорд сервере PoopLand!', description = """Вы только-что зашли в Дискорд сервер проекта **PoopLand**. Пока у вас нет роли "Игрок". Она выдается в течении 6 часов. Мы предлагаем ознакомится с нашим проектом в ожидании этого момента""", colour = 5793266)
            DMembed.set_footer(text = 'Ниже вы можете выбрать конкретные пункты которые вас интересуют. Бот предоставит вам необходимые знания.')
            DMembed.set_image(url = 'https://cdn.discordapp.com/attachments/1004371026131562507/1067475537498476704/73b00ff5093f8e37.png')
            Select = disnake.ui.Select(
                        custom_id = 'welcome',
                        placeholder = "Выберите пункт",
                        options = [
                            disnake.SelectOption(label = "Что такое PoopBot?", value = "welcome1"),
                            disnake.SelectOption(label = "Памятка с назначениями каналов", value = "welcome2"),
                            disnake.SelectOption(label = "Особенности сервера", value = "welcome3")
                        ]
            )
            await member.send(embed = DMembed, components = [Select])
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(995379037407027270)
        if member.guild == guild:
            chL = self.bot.get_channel(1067468355461730384)
            Goodbye = disnake.Embed(title=f"{member.name} **покинул сервер!**",colour = 15548997)
            await chL.send(embed=Goodbye)

    @commands.Cog.listener()
    async def on_dropdown(self, inter):
        labels = inter.values[0]
        if inter.component.custom_id == 'welcome':
            embed = None
            if labels == 'welcome1':
                embed = disnake.Embed(description = """**PoopBot** - Многофунциональный бот, который старается, чтобы игроки могли без каких-либо проблем взаимодействовать друг с другом. Вы переодически будете иметь дело с ним. Он имеет функции создания приватных войсов, автореакций, автоветок. Это поможет вам создать базовый дискорд для своего города без особых усилий. Подробнее о возможностях PoopBot`а можно узнать использовав команду </помощь:1038437698576339015>""", colour = 5793266)

            if labels == 'welcome2':
                embed = disnake.Embed(description = """<#995744032586215505> В закрепе сборка модов.
    <#1004371026131562506> Тут ты можешь ознакомиться с правилами.
    <#995747048487927858> После верификации ты можешь создать тикет гидам и они проведут тебе экскурсию по серверу. 
    <#1001920807414538311> Загляни сюда и возьми необходимые роли.
    Так как наступила зима админ дискорда добавил роли которые будут показывать рядом с твоим ником значок той роли которую ты выбрал, у меня роль"снежинка"  и рядом с моим ником изображена ❄️
    <#995745499602767972> Здесь проводитятся наборы в город @Ищу город.
    <#1061689351836270632>  В этом канале вы можете задать вопрос связанный с сервером.
    <#1026449092961906698> Предназначены для того, чтобы игроки могли оставлять отзывы на работу работников гос. структур, а также на игроков, которые оказали вам какую-либо услугу.
    <#995745618033131590> Здесь игроки оповещают о своих @Ивенты .
    <#1006612059938639872> Здесь ты можешь предложить идеи для сервера или дискорда,они будут рассмотрены и приняты на собрании игроков. 
    <#1035477028104847410> Тут вы можете зарегистрировать свой город в будущем.
    <#995754609886887977> Тут ты можешь найти работу или нанять игрока для работы.
    <#995745322452127786> Здесь ты можешь купить или продать ресурсы.
    <#1023270409891758152> Тут содержится информация для получения паспорта.
    <#995744289520877578> Здесь ты можешь выкладывать картинки связанные с сервером.
    <#997439509811691550> В этом канале вы можете делиться между собой полезными текстурпаками.
    <#1049081667131801600> Канал , в котором на бесплатной основе можно рекламировать контент по Poop Land.
    <#997183244137152605> В этом канале вы можете предложить эмодзи для добавление на данный дискорд сервер.
    <#1016414695026065519> Здесь ты можешь оставлять свои работы арты сделаные на сервере. @Ценитель .

    **Так же в этих каналах есть дополнительные правила которые находятся в закрепах.**""", colour = 5793266)

            if labels == 'welcome3':
                embed = disnake.Embed(description = """**1.** На PoopLand нет централизированой торговой площадки(ТФ). Вместо этого у каждого города есть возможность открыть собственный магазин и продавать товары прямо в городе.

**2.** На PoopLand нельзя иметь более одной крупной фермы в городе одновременно. У каждого города имеется одна основная ферма, которую мэр регистрирует в специальном канале <#1000091104118591608>. Но крупные фермы можно менять. Также городам запрещено строить свои фермы далеко от города и передавать ресурсы с ферм на бесплатной основе союзным городам. Подробнее о фермах можно узнать в правилах <#1004371026131562506>

**3.** В отличии от других проектов сайта SPworlds, на PoopLand блюстителей порядка называют ПДшниками т.к. сама организация называется ПД(Полицейский Депортамент)""", colour = 5793266)
                embed.set_footer(text = 'Этот пункт может пополнятся со временем.')

            await inter.send(embed = embed)

    @commands.slash_command(name = 'верификация', description = 'Команда для отправки сообщения верефицирующего в ДС', guild_ids = [762719493964169246])
    async def verify(self, interaction):
        embed = disnake.Embed(title = 'Верификация на сервере', description = 'Если в ДС PoopLand у вас есть роль игрока, нажмите на кнопку чтобы пройти верификацию', colour = 5793266)
        button = disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = 'Верифицироваться', custom_id = 'welcome_verify')
        await interaction.send(embed = embed, components = button)

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        pl_guild = self.bot.get_guild(995379037407027270)
        role_user0 = disnake.utils.get(pl_guild.roles,id = 995736158107611156)
        role_user1 = disnake.utils.get(pl_guild.roles,id = 1039589938670346271)
        roleJ = disnake.utils.get(interaction.guild.roles,id = 1040352751252684800)
        role_group1 = disnake.utils.get(interaction.guild.roles,id = 1141401549696946176)
        role_group2 = disnake.utils.get(interaction.guild.roles,id = 1141401572245504301)
        user = disnake.utils.get(pl_guild.members, id=interaction.author.id)
        if interaction.component.custom_id == 'welcome_verify':
            if role_user0 in user.roles or role_user1 in user.roles:
                await interaction.send('Роль ученика выдана', ephemeral = True)
                await interaction.author.add_roles(roleJ)

                if len(role_group1.members) < len(role_group2.members):
                    await interaction.author.add_roles(role_group1)
                    await interaction.send('Вы были зачислены в первую группу', ephemeral = True)
                elif len(role_group2.members) > len(role_group1.members):
                    await interaction.author.add_roles(role_group2)
                    await interaction.send('Вы были зачислены во вторую группу', ephemeral = True)
                elif len(role_group1.members) == len(role_group2.members):
                    await interaction.author.add_roles(role_group1)
                    await interaction.send('Вы были зачислены в первую группу', ephemeral = True)
                else:
                    await interaction.send('Не удалось зачислить вас в одну из групп. Напишите тапку. Он всё порешает.', ephemeral = True)
            
            else:
                await interaction.send('Не удалось найти у вас роль игрока в ДС PoopLand. Если она есть. Напишите Тапку', ephemeral = True)
                

        


def setup(bot):
    bot.add_cog(Welcome(bot))
