import io
import json

import disnake
import chat_exporter

from disnake.ext import commands

def load_json(filename):
    with open(filename, encoding="utf-8") as infile:
        return json.load(infile)


def write_json(filename, content):
    with open(filename, "w") as outfile:
        json.dump(content, outfile, ensure_ascii=True, indent=4)
class ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.zaversh = disnake.ui.Button(
            style = disnake.ButtonStyle.red,
            label = 'Закрыть',
            custom_id = 'Завершить'
        )
        
        self.yes_no = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = disnake.ButtonStyle.green,
                label = 'Да',
                custom_id = 'Да'
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.red,
                label = 'Нет',
                custom_id = 'Нет'
            )
        )

        self.delete = disnake.ui.Button(
            style = disnake.ButtonStyle.red,
            label = 'Удалить тикет',
            custom_id = 'Удалить'
        )

        
        self.button1 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = '<:discord:1007966414101028945>',
                custom_id = "Администрация Discord"
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = "<:poop:1007966412817563729>",
                custom_id = "Администрация Сервера"
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = "<:detective:1007966411525726218>",
                custom_id = "Детектив"
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = "<:siren:1007966670461091860>",
                custom_id = "ПД"
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = "<:briefcase_1f4bc:1019280018221830324>",
                custom_id = "Адвокат"
            )
        )
        self.button2 = disnake.ui.ActionRow(   
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = "🪙",
                custom_id = "Банкир"
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = "🚩",
                custom_id = "Гид"
            ),
            disnake.ui.Button(
                style= disnake.ButtonStyle.gray,
                emoji = '<:scroll_1f4dc:1065300438188040262>',
                custom_id = 'Паспортист'
            ),
            disnake.ui.Button(
                style= disnake.ButtonStyle.gray,
                emoji = '<:pill_1f48a:1065303089852190770>',
                custom_id = 'Врач'
            ),
            disnake.ui.Button(
                style= disnake.ButtonStyle.gray,
                emoji = '📊',
                custom_id = 'Министр Финансов'
            )
        )
        self.button2 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = disnake.ButtonStyle.gray,
                emoji = "📦",
                custom_id = "Почтальон"
            )
        )
        
    async def create_tickets(self, interaction, name: str, moderation: list, spectator: list, description: str, url: str, number: int):
            caty = disnake.utils.get(interaction.guild.categories, id = 995741752533209258)
            embed = disnake.Embed(title = name, description = description, color = disnake.Colour(0x2f3136))
            embed.set_thumbnail(url = url)
            user = interaction.author
            log_channel = interaction.guild.get_channel(995744203940311170)
            
            load = load_json('ticket.json')
            numbers = load[number]
            load[number] += 1
            write_json('ticket.json', load)
            moderation_mention = self.mention_panel(moderation = moderation)
            ticket_chl = await interaction.guild.create_text_channel(name = 'тикет-{:04d}'.format(numbers),topic = f'{interaction.component.custom_id}&{interaction.author.id}', category = caty)
            await ticket_chl.set_permissions(target = user, view_channel = True)
            for i in spectator:
                spectator_role = interaction.guild.get_role(i)
                await ticket_chl.set_permissions(target = spectator_role, view_channel = True)
            await ticket_chl.send(f'{interaction.author.mention}\n{moderation_mention}', embed = embed, components = [self.zaversh])
            await interaction.send(f'<#{ticket_chl.id}> создан', ephemeral = True)
            log_open_embed = disnake.Embed(description = f'**Тема:** {interaction.component.custom_id}\n**Обратился:** {interaction.author.mention}\n**Канал:** {ticket_chl.name}', colour = 3908956)
            log_open_embed.set_author(name = f'{interaction.author} открыл(а) тикет')
            await log_channel.send(embed = log_open_embed)

    def mention_panel(self, moderation):
            mention = ''
            for i in moderation:
                mention += f'<@&{i}>,\n'
            return mention


       
    @commands.slash_command()
    async def create_ticket(self, inter):
        create_button = disnake.ui.ActionRow(
            disnake.ui.Button(style= disnake.ButtonStyle.gray, label = 'Тема', custom_id = 'Тема_Тикет'),
            disnake.ui.Button(style= disnake.ButtonStyle.gray, label = 'Модератор', custom_id = 'Модератор_Тикет'),
            disnake.ui.Button(style= disnake.ButtonStyle.gray, label = 'Наблюдатель', custom_id = 'Наблюдатель_Тикет'),
            disnake.ui.Button(style= disnake.ButtonStyle.gray, label = 'Текст', custom_id = 'Текст_Тикет'),
            disnake.ui.Button(style= disnake.ButtonStyle.gray, label = 'Url', custom_id = 'Url_Тикет'),
        )
        create_embed = disnake.Embed(title = 'Добавить Тикет', description = """Тема: `None`

Модератор: `None`

Наблюдатель: `None`

Текст: `None`

Url: `None`""", color = disnake.Colour(0x2f3136))
        await inter.send(embed = create_embed, components = create_button)

    @commands.slash_command()
    @commands.has_any_role(743806507614994557, 719941717280948298, 995739756581355601)
    async def tickets(self, inter):
        dash_tp_emb = disnake.Embed(title = 'Тех. Поддержка', description = """<:discord:1007966414101028945> **Администрация Discord**

<:poop:1007966412817563729> **Администрация Сервера**

<:detective:1007966411525726218> **Детектив**

<:siren:1007966670461091860> **ПД**

<:briefcase_1f4bc:1019280018221830324> **Адвокат**

🪙 **Банкир**

🚩 **Гид**

<:scroll_1f4dc:1065300438188040262> **Паспортист**

<:pill_1f48a:1065303089852190770> **Врач**

📊 **Министр Финансов**

📦 **Почтальон**
""", color = disnake.Colour(0x2f3136))
        dash_tp_emb.set_footer(text = 'Чтобы открыть тикет, нажмите на кнопку')
        await inter.send(embed = dash_tp_emb, components = [self.button1, self.button2, self.button3])
  
        

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        log_chl = inter.guild.get_channel(995744203940311170)
        
        if inter.component.custom_id == 'Администрация Discord':
            await self.create_tickets(
                interaction = inter,
                name = 'Администрация Discord',
                moderation = [995739756581355601],
                spectator = [995739756581355601],
                description = 'Пока ожидаете ответа подробно опишите свою проблему/идею',
                url = 'https://cdn.discordapp.com/attachments/888870715879739411/1007959929816109096/discord.png', 
                number = '1'
            )
        
        if inter.component.custom_id == 'Администрация Сервера':
            await self.create_tickets(
                interaction = inter,
                name = 'Администрация Сервера',
                moderation = [997939231529898126],
                spectator = [997939231529898126],
                description = 'Пока ожидаете ответа подробно опишите свою проблему и при наличии приготовьте скрины/координаты.',
                url = 'https://cdn.discordapp.com/attachments/888870715879739411/1007961307842101268/poop.png', 
                number = '2'
            )
        
        if inter.component.custom_id == 'Детектив':
            await self.create_tickets(
                interaction = inter,
                name = 'Детектив',
                moderation = [995744050143580161],
                spectator = [995744050143580161],
                description = 'Пока ожидаете ответа напишите куда подъехать детективу.',
                url = 'https://cdn.discordapp.com/attachments/888870715879739411/1007962890290073640/detective.png', 
                number = '3'
            )

        if inter.component.custom_id == 'ПД':
            await self.create_tickets(
                interaction = inter,
                name = 'ПД',
                moderation = [995743116118204506],
                spectator = [995743116118204506],
                description = 'Пока ожидаете ответа напишите куда подъехать сотруднику ПД.',
                url = 'https://cdn.discordapp.com/attachments/888870715879739411/1007966709208064131/siren.png', 
                number = '4'
            )
    
        if inter.component.custom_id == 'Адвокат':
            await self.create_tickets(
                interaction = inter,
                name = 'Адвокат',
                moderation = [1016719349156954113],
                spectator = [1016719349156954113],
                description = 'Пока ожидаете ответа опишите проблему',
                url = 'https://cdn.discordapp.com/attachments/888870715879739411/1019279991634149396/briefcase_1f4bc.png', 
                number = '5'
            )

        if inter.component.custom_id == 'Банкир':
            await self.create_tickets(
                interaction = inter,
                name = 'Банкир',
                moderation = [995743178965651456],
                spectator = [995743178965651456],
                description = 'Пока ожидаете ответа напишите куда нужно подъехать банкиру',
                url = 'https://cdn.discordapp.com/attachments/1016391330643062808/1036310547840376892/coin_1fa99.png', 
                number = '6'
            )
        
        if inter.component.custom_id == 'Гид':
            await self.create_tickets(
                interaction = inter,
                name = 'Гид',
                moderation = [1033477685596409977],
                spectator = [1033477685596409977],
                description = 'Пока ожидаете ответа напишите куда нужно подъехать гиду',
                url = 'https://cdn.discordapp.com/attachments/1016391331133804671/1036312258302722078/triangular-flag_1f6a9.png', 
                number = '7'
            )

        if inter.component.custom_id == 'Паспортист':
            await self.create_tickets(
                interaction = inter,
                name = 'Паспортист',
                moderation = [1023278766518194249],
                spectator = [1023278766518194249],
                description = 'Пока ожидаете ответа напишите какой документ вам необходимо получить.',
                url = 'https://cdn.discordapp.com/attachments/1004371026131562507/1065299912687890492/scroll_1f4dc.png', 
                number = '8'
            )
        
        if inter.component.custom_id == 'Врач':
            await self.create_tickets(
                interaction = inter,
                name = 'Врач',
                moderation = [1006932328502800434],
                spectator = [1006932328502800434],
                description = 'Пока ожидаете ответа напишите куда подъехать врачу.',
                url = 'https://cdn.discordapp.com/attachments/1004371026131562507/1065299912687890492/scroll_1f4dc.png', 
                number = '9'
            )

        if inter.component.custom_id == 'Министр Финансов':
            await self.create_tickets(
                interaction = inter,
                name = 'Министр Финансов',
                moderation = [995742798554869830],
                spectator = [995742798554869830],
                description = 'Пока ожидаете ответа, начните свое обращение к Министру Финансов',
                url = 'https://cdn.discordapp.com/attachments/764243842869231616/1091415923753226291/bar-chart_1f4ca.png', 
                number = '10'
            )
        if inter.component.custom_id == 'Почтальон':
            await self.create_tickets(
                interaction = inter,
                name = "Почтальон",
                moderation = [1175083111848104011],
                spectator = [1175083111848104011, 1064273933714587768],
                description = 'Пока ожидаете ответа, начните свое обращение к Почтальону',
                url = 'https://media.discordapp.net/attachments/995746452104020069/1175008188567928882/package_1f4e6.png?ex=6569aaa6&is=655735a6&hm=87b09c7a81fba02479525e4f160f12782b6a8d73657fc86db10a167bc9273c60&=&width=480&height=480',
                number = '11'
            )

    

        if inter.component.custom_id == 'Завершить':
            zaver = disnake.Embed(title = f'{inter.author.name}, вы действительно хотите закрыть тикет?', color = disnake.Colour(0x2f3136))
            zaversh = await inter.send(embed = zaver, components = [self.yes_no])
        
        if inter.component.custom_id == 'Да':
            channelID = inter.channel.id
            c = inter.channel.topic
            topic = c.split('&')[0]
            obrID = c.split('&')[1]
            obr = await inter.guild.fetch_member(obrID)
            await inter.channel.set_permissions(target = obr, view_channel = False)
            yes = disnake.Embed(title = f'Тикет закрыт {inter.author.mention}', colour = 15548997)
            number = inter.channel.name[-4:]
            await inter.channel.edit(name = f'закрыт-{number}')
            await inter.message.delete()
            dels = await inter.send(embed = yes, components = [self.delete])
        
        if inter.component.custom_id == 'Нет':
            await inter.message.delete()
        
        if inter.component.custom_id == 'Удалить':
            delete = disnake.Embed(title = 'Тикет удалится в ближайшее время', color = disnake.Colour(0x2f3136))
            await inter.message.edit(embed = delete, components = None)
            channelID = inter.channel.id
            c = inter.channel.topic
            topic = c.split('&')[0]
            obrID = c.split('&')[1]
            await inter.send('Тикет закрыт', ephemeral = True)
            obr = await inter.guild.fetch_member(obrID)
            delete_log = disnake.Embed(description = f'**Тема:** {topic}\n**Обратился:** {obr}\n**Канал:** {inter.channel.name}', colour = 15548997)
            delete_log.set_author(name = f'{inter.author} закрыл(а) тикет')
            transcript = await chat_exporter.export(inter.channel)
            if transcript is None:
                return
            transcript_file = disnake.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{inter.channel.name}.html",
            )
            await log_chl.send(embed = delete_log, file = transcript_file)
            await inter.channel.delete()   

            


def setup(bot):
    bot.add_cog(ticket(bot))
