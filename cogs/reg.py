import disnake
from disnake.ext import commands
from disnake.utils import get

class SReg(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def create_button(self, inter, custom_id: str, label: str, emoji):
        button = disnake.ui.Button(
            style = disnake.ButtonStyle.gray,
            label = label,
            emoji = emoji,
            custom_id = custom_id
        )
        return button

    async def sends(self, interaction, registered):
        avatar_url = interaction.author.avatar
        if avatar_url == None:
            avatar_url = 'https://media.discordapp.net/attachments/780806472619261982/968208976095350835/1636180728_64-papik-pro-p-logotip-diskord-foto-67.png'
        text = ''
        for component in interaction.text_values:
            text += f'**{component}**:\n`{interaction.text_values[component]}`\n'

        embed = disnake.Embed(description = f'{interaction.author.mention} **зарегистрировал(а) {registered}**\n\n{text}', color = disnake.Colour(0x2f3136))
        embed.set_thumbnail(url = f'{avatar_url}')
        await interaction.message.thread.send(embed = embed)
        await interaction.send('**Заявка успешно подана**', ephemeral = True)
                
    async def send_modal(self, inter, custom_id: str, text_input: str = []):
        options = []
        for text in text_input:
            options.append(text)
        await inter.response.send_modal(title = 'Подача заявки', custom_id = custom_id, components = options)
                  
    @commands.slash_command()
    async def reg(self, inter, ed = None):
        
        emb = disnake.Embed(title = 'Дорогие будущие мэры городов!', description = """
Здесь вы можете зарегистрировать свой город.
Для этого необходимо нажать на кнопку под этим сообщением и заполнить заявку по форме.

**1.** Название города
**2.** Описание
**3.** Список
**4.** Координаты верхний мир
**5.** Координаты ад

Если заявка будет заполнена не верно, либо если в вашем городе проживает менее 5 граждан, **регистрацию удалят**.

Если вы являетесь жителем какого-либо города на сайте мы не сможем добавить ваш город на карту.
**Перед подачей заявки покиньте другие города!**""", color = disnake.Colour(0x2f3136))
        emb2 = disnake.Embed(title = '', description= '', color = disnake.Colour(0x2f3136))
        emb2.set_image(url = 'https://cdn.discordapp.com/attachments/995379037407027273/1035551324084895794/630453818105b7f4.png')
        
        
        city_msg = await inter.channel.fetch_message(1035557643584024586)
        if ed is None:
            msg = await inter.channel.send(embeds = [emb2,emb], components = self.create_button(inter = inter, custom_id = 'reg1', label = 'Регистрация', emoji = '🖊️'))
            await msg.channel.create_thread(name = 'Города 🌆', message = msg)
        if ed is not None:
            msg = await city_msg.edit(embeds = [emb2, emb], components = self.create_button(inter = inter, custom_id = 'reg1', label = 'Регистрация', emoji = '🖊️'))
            
    @commands.slash_command()
    async def base(self, inter):
        emb = disnake.Embed(title = 'Дорогие владельцы баз!', description = """
Здесь вы можете зарегистрировать свою базу.
Для этого необходимо нажать на кнопку под этим сообщением и заполнить заявку по форме.

1. Ваш ник
2. Координаты портала в верхнем мире
3. Координаты портала в аду

Если заявка будет заполнена не верно, **регистрацию удалят**.""", color = disnake.Colour(0x2f3136))
        emb2 = disnake.Embed(title = '', description= '', color = disnake.Colour(0x2f3136))
        emb2.set_image(url = 'https://cdn.discordapp.com/attachments/1004371026131562507/1079049568353779762/base.png')
        msg = await inter.channel.send(embeds = [emb2,emb], components = self.create_button(inter = inter, custom_id = 'reg3', label = 'Регистрация', emoji = '🖊️'))
        await msg.channel.create_thread(name = 'Базы 🌆', message = msg)


    @commands.slash_command()
    async def farm(self, inter):
        button = disnake.ui.Button(
            style = disnake.ButtonStyle.gray,
            label = 'Регистрация',
            emoji = '🖊️',
            custom_id = 'reg2'
        )
        emb = disnake.Embed(title = 'Дорогие мэры городов!', description = """Город может использовать только одну большую ферму в городе!

> Шаблон для определения фермы города:

**1.** Название Вашего города.
**2.** Укажите количество Ваших жителей в городе (минимально должно быть 8 человек и у всех одно гражданство).
**3.** Какая у вас ферма? 

Если происходит замена фермы пишите в скобках (Замена).""", color = disnake.Colour(0x2f3136))
        msg = await inter.channel.send(embed = emb, components = self.create_button(inter = inter, custom_id = 'reg2', label = 'Регистрация', emoji = '🖊️'), file = disnake.File('farm.png'))
        await msg.channel.create_thread(name = 'Фермы 🌆', message = msg)


    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id == 'reg1':
            components = [
                disnake.ui.TextInput(label = 'Название', custom_id = 'Название'),
                disnake.ui.TextInput(label = 'Описание', custom_id = 'Описание'),
                disnake.ui.TextInput(label = 'Список жителей', custom_id = 'Список жителей'),
                disnake.ui.TextInput(label = 'Координаты верхний мир', custom_id = 'Координаты верхний мир'),
                disnake.ui.TextInput(label = 'Координаты ад', custom_id = 'Координаты ад'),
            ]
            await self.send_modal(inter, 'city', components)
        
        if inter.component.custom_id == 'reg2':
            components=[
                disnake.ui.TextInput(label = 'Название Вашего города', custom_id = 'Название Вашего города'),
                disnake.ui.TextInput(label = 'Кол-во жителей в городе', custom_id = 'Кол-во жителей в городе'),
                disnake.ui.TextInput(label = 'Какая у вас ферма?', custom_id = 'Какая у вас ферма?'),
            ]
            await self.send_modal(inter, 'farm', components)
        
        if inter.component.custom_id == 'reg3':
            components=[
                disnake.ui.TextInput(label = 'Ваш ник', custom_id = 'Никнейм владельца'),
                disnake.ui.TextInput(label = 'Координаты портала в верхнем мире', custom_id = 'Координаты портала в верхнем мире'),
                disnake.ui.TextInput(label = 'Координаты портала в аду', custom_id = 'Координаты портала в аду'),
            ]
            await self.send_modal(inter, 'base', components)


    @commands.Cog.listener()
    async def on_modal_submit(self, inter):
        avatar_url = inter.author.avatar.url
        if avatar_url == None:
            avatar_url = 'https://cdn.discordapp.com/attachments/1004371026131562507/1035556570869805056/a109edc5db361bdf.png'
        if inter.custom_id == 'city':
            await self.sends(interaction = inter, registered = 'город')
        if inter.custom_id == 'farm':
            await self.sends(interaction = inter, registered = 'ферму')
        if inter.custom_id == 'base':
            await self.sends(interaction = inter, registered = 'базу')
        
        
def setup(bot):
    bot.add_cog(SReg(bot))     
