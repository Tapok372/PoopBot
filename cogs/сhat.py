import disnake
from disnake.ext import commands
from disnake import Localized, ButtonStyle
import sqlite3

class Chat(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.db = sqlite3.connect(f'PoopBot.db')
        self.table = self.db.cursor()
        self.row_of_buttons = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = "<:One:1039951224214130719>",
                custom_id = "hp1"
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = "<:Two:1039951222574174248>",
                custom_id = "hp2"
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = "<:Three:1039951220586074112>",
                custom_id = "hp3"
            ),
            disnake.ui.Button(
                style = ButtonStyle.gray,
                emoji = "<:Four:1039951219122253866>",
                custom_id = "hp4"
            )
        )
        self.back_button = disnake.ui.Button(
            style = ButtonStyle.gray,
            emoji = "<:Back:1038810328831631410>",
            custom_id = "hpb"
        )

    def convertion_emoji(self, emoji):
        if len(emoji) == 1:
                after = emoji
        elif len(emoji) > 1:
                Mystr = emoji.split(':')
                emojiID = Mystr[2][:-1]
                after = emojiID.replace(">", "") 

        return after

    def check_emoji(self, channel, emoji):
        self.table.execute("SELECT emoji FROM Reactions WHERE channelID = ?",(channel.id,))
        emoji_db = self.table.fetchall()
        print(f'{emoji}')
        print(f'{emoji_db}')
        action = False
        if emoji_db:
            for i in range(len(emoji_db)):
                emoji_db_after = emoji_db[i][0]
                if emoji_db_after != emoji:
                    action = False
                if emoji_db_after == emoji:
                    action = True
                    break
        
                
        return action

                

        

    @commands.slash_command(name = Localized("помощь", key="HELP_NAME"), description = Localized('Команда в которой описано то, как управлять функциями бота',key="HELP_DESCRIPTION"))
    async def help(self, inter,):
        embed = disnake.Embed(title = 'Панель помощи', description = """<:One:1039951224214130719> - Пункт в котором вы подробно можете узнать о том, как добавить автореакции в каналы сервера.

<:Two:1039951222574174248> - Пункт в котором вы поднробно узнаете о том, как добавлять автоветки в каналы сервера.

<:Three:1039951220586074112> - Пункт в котором вы узнаете о том, как добавить приватные голосовые каналы и то, какие функции вы имеете используя их.

<:Four:1039951219122253866> - Пункт в котором вы узнаете как подключить логирование на своем сервере""", colour = 3092790)
        embed_image = disnake.Embed( colour = 3092790)
        embed_image.set_image(url = 'https://cdn.discordapp.com/attachments/764243842869231616/1039957100379508756/HelpPanel.png')
        await inter.response.send_message(embeds = [embed_image, embed], components = self.row_of_buttons, ephemeral = True)


    @commands.slash_command(name = Localized("автореакции", key="REACT_NAME"), description = Localized('Команда для добавления автореакций в текстовые каналы',key="VOICE_DESCRIPTION"))
    @commands.has_permissions(manage_messages = True, manage_channels = True)
    async def autoreact(
        self,
        inter,
        stat: str = commands.Param(
            choices=["Добавить", "Удалить"],
            name=Localized('действие',key="STAT_NAME"),
            description=Localized('Выберите действие',key="STAT_DESCRIPTION")),
        channel: disnake.TextChannel = commands.Param(
            name=Localized('канал',key="CHANNEL_NAME"),
            description=Localized('Выберите канал в котором хотите включить или выключить автореакции',key="CHANNEL_DESCRIPTION")),
        emojis: str = commands.Param(
            name=Localized('эмодзи',key="CHANNEL_NAME"),
            description=Localized('Выберите эмодзи которое нужно ставить в канале',key="CHANNEL_DESCRIPTION")),
    ):
        log_channel = self.bot.get_channel(764243467139416064)
        guildID = inter.guild.id
        channelID = channel.id
        emoji = self.convertion_emoji(emoji = emojis)
        action = self.check_emoji(channel = channel, emoji = emoji)
        print(action)
        if ";" in emojis:
            await inter.send("SQL инъекции запрещены", ephemeral = True)
        else:
            if action is True:
                if stat == 'Добавить':
                    await log_channel.send(f'{inter.author} попытался добавить реакцию в канал {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}. Но у него ничего не получилось.')
                    await inter.send(f'Эта реакция уже добавлена в канал {channel.mention}', ephemeral = True)
                if stat == 'Удалить':
                    self.table.execute('DELETE FROM Reactions WHERE emoji=?', (emoji,))
                    self.db.commit()
                    await log_channel.send(f'{inter.author} удалил реакцию {emoji} из канала {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}.')
                    await inter.send(f'Эмодзи {emoji} удалена из автореакций канала {channel.mention}', ephemeral = True)

            elif action is False:
                if stat == 'Добавить':
                    self.table.execute("INSERT INTO Reactions VALUES (?, ?, ?)",(guildID, channelID, emoji,))
                    self.db.commit()
                    await log_channel.send(f'{inter.author} добавил реакцию {emoji} в канал {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}.')
                    await inter.send(f'Эмодзи {emoji} добавлена в автореакции канала {channel.mention}', ephemeral = True)
                if stat == 'Удалить':
                    await log_channel.send(f'{inter.author} попытался удалить реакцию из канала {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}. Но у него ничего не получилось.')
                    await inter.send(f'Этой реакции нет в списке автореакции канала {channel.mention}', ephemeral = True)
        
            self.db.commit()
    @commands.slash_command(name = Localized("ветки", key="THREAD_NAME"), description = Localized('Команда для добавления автоветок в текстовые каналы',key="THREAD_DESCRIPTION"))
    @commands.has_permissions(manage_messages = True, manage_channels = True)
    async def autothread(
        self,
        inter,
        stat: str = commands.Param(
            choices=["Добавить", "Удалить"],
            name=Localized('действие',key="STAT_NAME"),
            description=Localized('Выберите действие',key="STAT_DESCRIPTION")),
        channel: disnake.TextChannel = commands.Param(
            name=Localized('канал',key="CHANNEL_NAME"),
            description=Localized('Выберите канал в котором хотите включить или выключить автореакции',key="CHANNEL_DESCRIPTION")),
        name: str = commands.Param(
            name=Localized('название',key="THREAD_NAME"),
            description=Localized('Выберите название ветки которую нужно создавать в канале',key="CHANNEL_DESCRIPTION")),
    ):
        channelID = channel.id
        names = name
        log_channel = self.bot.get_channel(764243467139416064)
        self.table.execute("SELECT name FROM Threads WHERE channelID = ? and name = ?",(channel.id,name,))
        name_bd = self.table.fetchone()
        if ";" in names:
            await inter.send("SQL инъекции запрещены", ephemeral = True)
        else:
            if name_bd:
                if stat == 'Добавить':
                    await log_channel.send(f'{inter.author} попытался добавить ветку в канал {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}. Но у него ничего не получилось.')
                    await inter.send(f'Ветка уже добавлена в канал {channel.mention}', ephemeral = True)
                if stat == 'Удалить':
                    self.table.execute('DELETE FROM Threads WHERE name=?', (names,))
                    self.db.commit()
                    await log_channel.send(f'{inter.author} удалил ветку {name} из канала {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}.')
                    await inter.send(f'Автоветка с названием **{names}** удалена из канала {channel.mention}', ephemeral = True)

            if name_bd is None:
                guildID = inter.guild.id
                if stat == 'Добавить':
                    self.table.execute("INSERT INTO Threads VALUES (?, ?, ?)",(guildID, channelID, names,))
                    self.db.commit()
                    await self.log_channel.send(f'{inter.author} добавил ветку {name} в канал {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}.')
                    await inter.send(f'Автоветка с названием **{names}** добавлена в канал {channel.mention}', ephemeral = True)
                if stat == 'Удалить':
                    await self.log_channel.send(f'{inter.author} попытался удалить ветку из канала {inter.channel}|{inter.channel.id} дискорд сервера {inter.guild}|{inter.guild.id}. Но у него ничего не получилось.')
                    await inter.send(f'Этой автоветки нет в канале {channel.mention}', ephemeral = True)

            else:
                print('Error autothread')

    @commands.slash_command(name = Localized("баг-репорт", key="THREAD_NAME"), description = Localized('Используте эту команду если бот работает неисправно',key="THREAD_DESCRIPTION"))
    async def bag_report(self, inter, message):
        avatar_url = inter.author.avatar.url
        if avatar_url == None:
            avatar_url = 'https://media.discordapp.net/attachments/780806472619261982/968208976095350835/1636180728_64-papik-pro-p-logotip-diskord-foto-67.png'
        embed = disnake.Embed(title = f'Репорт от {inter.author}\{inter.author.id}', description = message, colour = 3092790)
        embed.set_thumbnail(url = avatar_url)
        channel = self.bot.get_channel(764243467139416064)
        await inter.response.send_message('Репорт отправлен создателю', ephemeral = True)
        await channel.send(embed = embed)

    @commands.Cog.listener(name = 'on_message')
    async def autoreactions(self, message):
        self.table.execute("SELECT emoji FROM Reactions WHERE channelID = ?",(message.channel.id,))
        massive = self.table.fetchall()
        try:
            if massive:
                for i in range(len(massive)):
                    inv = massive[i]
                    emoji = inv[0]
                    if len(str(emoji)) == 1:
                        await message.add_reaction(emoji)
                    elif len(str(emoji)) > 1:
                        react = await message.guild.fetch_emoji(emoji)
                        await message.add_reaction(react)
        except Exception as err:
            channel = self.bot.get_channel(764243467139416064)
            await channel.send(err)

    @commands.Cog.listener(name = 'on_message')
    async def autothreads(self, message):
        try:        
            self.table.execute("SELECT name FROM Threads WHERE channelID = ?",(message.channel.id,))
            thread = self.table.fetchall()
            for i in range(len(thread)):
                inv = thread[i]
                name = inv[0]
                await message.channel.create_thread(name = name, message = message, auto_archive_duration = 1440)
        except:
            channel = self.bot.get_channel(764243467139416064)
            await channel.send('В автоветках поломка')
        
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id == 'hp1':
            embed = disnake.Embed(title = 'Авто Реакции', description = """**Добро пожаловать во вкладку "Автореакции"**

__**Авто Реакция**__ - Функция которая позволяет вам добавлять реакции автоматически ко всем сообщениям отправляемым в канал после подключения функции.

> **Как подключить авто реакции к каналу?**

Для подключения необходимо ввести команду ```/автореакции``` 
**Эта команда имеет несколько аргументов:**

`действие` - Аргумент с выбором [Добавить/Удалить]. В зависимости от того, что вам необходимо сделать, добавить авто реакцию в канал (Добавить) или наоборот убрать ее (Удалить), вы выбираете действие.

`канал` - Аргумент с выбором канала, в котором будут ставиться авто реакции. Перед вами всплывет список из каналов сервера. Если какого-либо канала в этом списке нет, введите в аргумент названия канала, когда он появится в списке нажмите на него.

`эмодзи` - Аргумент в который вам необходимо ввести эмодзи, который бот будет ставить в выбранный вами канал. Эмодзи должен быть из сервера в котором есть Poop Bot.

`Команда работает только у людей с возможностью управлять сообщениями либо если у вас есть админка на роли`
Если у вас возникли вопросы, задвайте их <@469530841052086283>.""", colour = 3092790)
            embed_image = disnake.Embed(colour = 3092790)
            embed_image.set_image(url = 'https://cdn.discordapp.com/attachments/764243842869231616/1039956891972927600/AutoReact.png')
            await inter.response.edit_message(embeds = [embed_image,embed], components = self.back_button)
        if inter.component.custom_id == 'hp2':
            embed = disnake.Embed(title = 'Авто Ветки', description = """**Добро пожаловать во вкладку "Авто Ветки"**

__**Авто Ветки**__ - Функция которая позволяет вам добавлять ветки автоматически ко всем сообщениям отправляемым в канал после подключения функции.

> **Как подключить авто ветки к каналу?**

Для подключения необходимо ввести команду ```/ветки``` 
**Эта команда имеет несколько аргументов:**

`действие` - Аргумент с выбором [Добавить/Удалить]. В зависимости от того, что вам необходимо сделать, добавить авто ветку в канал (Добавить) или наоборот убрать ее (Удалить), вы выбираете действие.

`канал` - Аргумент с выбором канала, в котором будут ставиться авто ветки. Перед вами всплывет список из каналов сервера. Если какого-либо канала в этом списке нет, введите в аргумент названия канала, когда он появится в списке нажмите на него.

`название` - Аргумент в который вам необходимо ввести название, с которым бот будет создаваться ветка в выбранном канале.

`Команда работает только у людей с возможностью управлять сообщениями либо если у вас есть админка на роли`
Если у вас возникли вопросы, задавайте их <@469530841052086283>.""", colour = 3092790)
            embed_image = disnake.Embed(colour = 3092790)
            embed_image.set_image(url = 'https://cdn.discordapp.com/attachments/764243842869231616/1039956891570290758/AutoThread.png')
            await inter.response.edit_message(embeds = [embed_image,embed], components = self.back_button)
        if inter.component.custom_id == 'hp3':
            embed = disnake.Embed(title = 'Приватные Войсы', description = """**Добро пожаловать во вкладку \"Приватные Войсы\"**

__**Приватные Войсы**__ - Функция которая создает категорию и канал для приватных каналов в вашем discord сервере.

> **Как подключить приватные войсы к серверу?**

Для подключения необходимо ввести команду ```/приватки``` 
При вводе этой команды, бот создаст категорию и канал которые сразу можно будет использовать. Войсами можно управлять с помощью панели, которая находится в текстовом чате созданной вами приватки.

`Команда работает только у людей с возможностью управлять сообщениями либо если у вас есть админка на роли`
Если у вас возникли вопросы, задвайте их <@469530841052086283>.""", colour = 3092790)
            embed_image = disnake.Embed(colour = 3092790)
            embed_image.set_image(url = 'https://cdn.discordapp.com/attachments/764243842869231616/1039956892677587024/HelpPrivat.png')
            await inter.response.edit_message(embeds = [embed_image,embed], components = self.back_button)
            
        if inter.component.custom_id == 'hpb':
            embed = disnake.Embed(title = 'Панель помощи', description = """<:One:1039951224214130719> - Пункт в котором вы подробно можете узнать о том, как добавить автореакции в каналы сервера.

<:Two:1039951222574174248> - Пункт в котором вы поднробно узнаете о том, как добавлять автоветки в каналы сервера.

<:Three:1039951220586074112> - Пункт в котором вы узнаете о том, как добавить приватные голосовые каналы и то, какие функции вы имеете используя их.

<:Four:1039951219122253866> - Пункт в котором вы узнаете как подключить логирование на своем сервере""", colour = 3092790)
            embed_image = disnake.Embed( colour = 3092790)
            embed_image.set_image(url = 'https://cdn.discordapp.com/attachments/764243842869231616/1039957100379508756/HelpPanel.png')
            await inter.response.edit_message(embeds = [embed_image, embed], components = self.row_of_buttons)

        if inter.component.custom_id == 'hp4':
            embed = disnake.Embed(title = 'Логирование',  description = """**Добро пожаловать во вкладку "Логирование"**

__**Логирование**__ - Функция которая создает категорию и канал для приватных каналов в вашем discord сервере.

> **Как подключить логирование к серверу?**

Для подключения необходимо ввести команду ```/логи``` 

**Эта команда имеет несколько аргументов:**

`логирование` - Аргумент в с выбором вида логирования [Логи Сообщений/Логи Войсов/Логи Игроков]

`канал` - Аргумент с выбором канала, в который будут приходить логи со всего сервера. Перед вами всплывет список из каналов сервера. Если какого-либо канала в этом списке нет, введите в аргумент названия канала, когда он появится в списке нажмите на него.

`действия` - Аргумент с выбором [Подключить/Отключить]. В зависимости от того, что вам необходимо сделать, добавить логирование к каналу или наоборот отключить его.


Если у вас возникли вопросы, задвайте их @Tapok#4970.""", colour = 3092790)
            embed_image = disnake.Embed(colour = 3092790)
            embed_image.set_image(url = 'https://cdn.discordapp.com/attachments/764243842869231616/1039956892350427237/HelpLogging.png')
            await inter.response.edit_message(embeds = [embed_image,embed], components = self.back_button)


def setup(bot):
    bot.add_cog(Chat(bot))
