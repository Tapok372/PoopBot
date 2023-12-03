import disnake
import sqlite3
from disnake.ext import commands
from utils import private


class voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect(f'voice.db')
        self.table = self.db.cursor()
        self.private = private.Voice
        self.embed = disnake.Embed(title = f"Управление приватными комнатами", description = """**Вы можете изменить конфигурацию своей комнаты с помощью кнопок ниже.**
        
<:tops:1074249572999766066> — Назначить нового владельца приватной комнаты

<:rename:1074249585612029952> — Переименовать приватную комнату

<:limit:1074249577563173004> — Задать лимит участников приватной комнаты

<:lock:1074249584278257746> — Закрыть/Открыть приватную комнату

<:visibility:1074249581484855347> — Скрыть/Открыть приватную комнату

<:doors:1074249580243337226> — Кикнуть пользователя из войса

<:whitelist:1074251690322165790>  — Добавить пользователя в white list канала

<:claim:1074249575843512330> — Забрать права на канал""", color = disnake.Colour(0x2f3136))
        self.components1 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:tops:1074249572999766066>',
                custom_id = 'claim' 
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:rename:1074249585612029952>',
                custom_id = 'rename' 
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:limit:1074249577563173004>',
                custom_id = 'limit' 
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:lock:1074249584278257746>',
                custom_id = 'lock' 
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:visibility:1074249581484855347>',
                custom_id = 'visibility' 
            )
        )
        self.components2 = disnake.ui.ActionRow(
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:doors:1074249580243337226>',
                custom_id = 'kick' 
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:whitelist:1074251690322165790>',
                custom_id = 'whitelist' 
            ),
            disnake.ui.Button(
                style = disnake.ButtonStyle.grey,
                emoji = '<:claim:1074249575843512330>',
                custom_id = 'blood_claim' 
            )
        )
    
    @commands.slash_command(name = 'приватки', description = 'Команда для подключения приватных войсов к вашему дискорд серверу')
    @commands.has_permissions(manage_messages = True, manage_channels = True)
    async def private_voice(
        self,
        inter,
        caty = commands.Param(name = 'категория', description = 'Введите название для категории. После подключения приватных войсов её можно будет изменить.'),
        channel = commands.Param(name = 'канал', description = 'Введите название канала при входе в который будет создаваться приватный канал.')
    ):
        if len(caty) >= 100 or len(caty) <= 0 and len(channel) >= 100 or len(channel) <= 0:
            await inter.send('**ОШИБКА: Название категории или канала не должно быть короче одного симовола или привышать сто символов. Попробуйте сократить количество символов в названии.**', ephemeral = True)
        else:
            self.table.execute("DELETE FROM VoiceCreator WHERE guildID = ?",(inter.guild.id,))
            self.db.commit()
            category = await inter.guild.create_category(name = caty)
            voice_channel = await inter.guild.create_voice_channel(name = channel, category = category)
            self.table.execute("INSERT INTO VoiceCreator VALUES (?, ?, ?)",(int(inter.guild.id), int(category.id), int(voice_channel.id),))
            self.db.commit()
            await inter.send(f'**Вы успешно подключили приватные каналы к своему серверу. Можете сразу опробовать их зайдя в войс <#{voice_channel.id}>**', ephemeral = True)
        
        self.db.commit()
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        vision = 'Виден'
        access = 'Открыт'
        name = await self.private.name_channel_check(self, member = member.id)
        
        if after.channel and after.channel != before.channel:
            self.table.execute("SELECT * FROM VoiceCreator WHERE guildID = ?",(member.guild.id,))
            massive = self.table.fetchone()
            category = disnake.utils.get(member.guild.categories, id = massive[1])
            if after.channel.id == massive[2]:
                voice = await member.guild.create_voice_channel(name = name, category = category)
                await voice.set_permissions(member, view_channel = True, connect = True, manage_channels = True)
                await member.move_to(voice)
                Panel = disnake.Embed(title = 'Информация о канале', description = f'**Владелец:** {member.mention}\n**Видимость:** Виден\n**Досупность:** Открыт', color = disnake.Colour(0x2f3136))
                await voice.send(embeds = [Panel, self.embed], components = [self.components1, self.components2])
                self.table.execute("INSERT INTO VoiceChannels VALUES (?, ?, ?, ?)",(member.id, vision, access, voice.id,))
                self.db.commit()

        if before.channel and before.channel != after.channel:
            self.table.execute("SELECT * FROM VoiceCreator WHERE guildID = ?",(member.guild.id,))
            massive = self.table.fetchone()
            if massive:
                if before.channel.id != massive[2] and before.channel.category.id == massive[1]:
                    if len(before.channel.members) == 0:
                        await before.channel.delete()
                        self.table.execute('DELETE FROM VoiceChannels WHERE voiceID = ?', (before.channel.id,))
                        self.db.commit()


    @commands.Cog.listener()
    async def on_button_click(self, inter):
        self.table.execute("SELECT * FROM VoiceCreator WHERE guildID = ?",(inter.guild.id,))
        massive = self.table.fetchone()
        if inter.channel.category.id == massive[1] and inter.author.voice is not None:
            VoiceChannelID = inter.channel.id
            self.table.execute("SELECT * FROM VoiceChannels WHERE voiceID = ?",(VoiceChannelID,))
            voice_channel = self.table.fetchone()
            
            if inter.channel.category.id == massive[1] and str(voice_channel[0]) != str(inter.author.id) and inter.component.custom_id != 'blood_claim':
                await inter.send('**У вас нет прав на этот канал**', ephemeral = True)
            
            elif inter.component.custom_id == 'claim' and str(voice_channel[0]) == str(inter.author.id):
                await inter.send('**Пинганите нового владельца войса**', ephemeral = True)
                def check(message):
                    return str(message.author.id) == str(voice_channel[0])
                owner_message = await self.bot.wait_for('message',timeout=60 ,check=check)
                if ";" in owner_message.content:
                    await inter.send("SQL инъекции запрещены", ephemeral = True)
                else:
                    owner = owner_message.content[:-1][2:]
                    await owner_message.delete()
                    before_owner = await self.bot.fetch_user(voice_channel[0])
                    try:
                        after_owner = await self.bot.fetch_user(owner)
                        await inter.channel.set_permissions(after_owner, view_channel = True, connect = True, manage_channels = True)
                        await inter.channel.set_permissions(before_owner, view_channel = None, connect = None, manage_channels = None)
                        self.table.execute("UPDATE VoiceChannels SET owner = ? WHERE voiceID = ?",(owner, voice_channel[3],))
                        self.db.commit()
                        await inter.send(f'**<@{owner}> назначен(а) новым владельцем канала {inter.channel.name}**', ephemeral = True)
                        await self.private.voice_panel_edit(self, inter = inter)
                    except disnake.errors.HTTPException:
                        await inter.send('**ОШИБКА: Необходимо упомянуть участника, которому вы хотите передать права. Нажмите на кнопку ещё раз и пинганите участника**', ephemeral = True)
                
            
            elif inter.component.custom_id == 'rename' and str(voice_channel[0]) == str(inter.author.id):
                await inter.send('**Введите новое название войса**', ephemeral = True)
                def new_name(message):
                    return str(message.author.id) == str(voice_channel[0])
                name_message = await self.bot.wait_for('message',timeout=60 ,check=new_name)
                name = name_message.content
                await name_message.delete()
                if ";" in name:
                    await inter.send("SQL инъекции запрещены", ephemeral = True)

                elif len(name) >= 100 or len(name) <= 0:
                    await inter.send('**ОШИБКА: Название войса не должно быть короче одного симовола или привышать сто символов. Нажмите на кнопку ещё раз и введите название, которое будет соотвествовать требованиям**', ephemeral = True)
                else:
                    await inter.channel.edit(name = name)
                    await inter.send(f'**Вы успешно изменили название канала на:** {name}', ephemeral = True)
                    await self.private.name_channel_check(self, member = inter.author.id, name = name)
            
            elif inter.component.custom_id == 'limit' and str(voice_channel[0]) == str(inter.author.id):
                await inter.send('**Введите новый лимит войса**', ephemeral = True)
                def new_limit(message):
                    return str(message.author.id) == str(voice_channel[0])
                limit_message = await self.bot.wait_for('message',timeout=60 ,check=new_limit)
                limit = limit_message.content
                await limit_message.delete()
                try:
                    if ";" in limit:
                        await inter.send("SQL инъекции запрещены", ephemeral = True)

                    elif int(limit) >= 100:
                        await inter.send('**Лимит не может быть больше 99 участников**', ephemeral = True)
                    else:
                        await inter.channel.edit(user_limit = limit)
                        await inter.send(f'**Вы успешно изменили лимит пользователей канала на:** {limit}', ephemeral = True)
                except ValueError:
                    await inter.send('**ОШИБКА: В заданном вами лимите используются недопустимые символы. Нажмите на кнопку ещё раз и введите число от 0 до 99**', ephemeral = True)
            elif inter.component.custom_id == 'lock' and str(voice_channel[0]) == str(inter.author.id):
                if voice_channel[2] == 'Открыт':
                    access = 'Закрыт'
                    self.table.execute("UPDATE VoiceChannels SET access = ? WHERE voiceID = ?",(access, voice_channel[3],))
                    self.db.commit()
                    await inter.channel.set_permissions(inter.guild.default_role, connect=False)
                    await inter.send('**Вы успешно закрыли канал**', ephemeral = True)
                if voice_channel[2] == 'Закрыт':
                    access = 'Открыт'
                    self.table.execute("UPDATE VoiceChannels SET access = ? WHERE voiceID = ?",(access, voice_channel[3],))
                    self.db.commit()
                    await inter.channel.set_permissions(inter.guild.default_role, connect=True)
                    await inter.send('**Вы успешно открыли канал**', ephemeral = True)
                await self.private.voice_panel_edit(self, inter = inter)
            
            elif inter.component.custom_id == 'visibility' and str(voice_channel[0]) == str(inter.author.id):
                if voice_channel[1] == 'Виден':
                    visibility = 'Скрыт'
                    self.table.execute("UPDATE VoiceChannels SET vision = ? WHERE voiceID = ?",(visibility, voice_channel[3],))
                    self.db.commit()
                    await inter.channel.set_permissions(inter.guild.default_role, view_channel=False)
                    await inter.send('**Вы успешно скрыли канал**', ephemeral = True)
                if voice_channel[1] == 'Скрыт':
                    visibility = 'Виден'
                    self.table.execute("UPDATE VoiceChannels SET vision = ? WHERE voiceID = ?",(visibility, voice_channel[3],))
                    self.db.commit()
                    await inter.channel.set_permissions(inter.guild.default_role, view_channel=True)
                    await inter.send('**Вы успешно открыли канал**', ephemeral = True)
                await self.private.voice_panel_edit(self, inter = inter)
            
            elif inter.component.custom_id == 'kick' and str(voice_channel[0]) == str(inter.author.id):
                await inter.send('Пинганите человека которого хотите кикнуть из войса', ephemeral = True)
                def kick_user(message):
                    return str(message.author.id) == str(voice_channel[0])
                kick_message = await self.bot.wait_for('message',timeout=60 ,check=kick_user)
                if ";" in kick_message.content:
                    await inter.send("SQL инъекции запрещены", ephemeral = True)
                else:
                    member_kickID = kick_message.content[:-1][2:]
                    await kick_message.delete()
                    await self.private.check_user_in_voice(self, inter, inter.channel.members, member_kickID)
                
            elif inter.component.custom_id == 'whitelist' and str(voice_channel[0]) == str(inter.author.id):
                await inter.send('**Пинганите человека которому вы бы хотели выдать особые права на вход**', ephemeral = True)
                def white_list(message):
                    return str(message.author.id) == str(voice_channel[0])
                white_message = await self.bot.wait_for('message',timeout=60 ,check=white_list)
                if ";" in white_message.content:
                    await inter.send("SQL инъекции запрещены", ephemeral = True)
                else:
                    white = white_message.content[:-1][2:]
                    await white_message.delete()
                    try:
                        user_white = await self.bot.fetch_user(white)
                        await inter.channel.set_permissions(user_white, connect=True, view_channel = True)
                        await inter.send(f'**Пользователь {user_white.mention} добавлен в белый список вашего войса**', ephemeral = True)
                    except disnake.errors.HTTPException:
                        await inter.send('**ОШИБКА: Необходимо упомянуть участника, которого хотите добавить в белый список канала. Нажмите на кнопку ещё раз и пинганите участника**', ephemeral = True)
                    

            elif inter.component.custom_id == 'blood_claim' and str(voice_channel[0]) != str(inter.author.id): 
                check = await self.private.check_owner_in_voice(self, inter = inter, members = inter.channel.members, voice = inter.channel.id)
                await self.private.voice_panel_edit(self, inter = inter)
            
            elif inter.component.custom_id == 'blood_claim' and str(voice_channel[0]) == str(inter.author.id):
                await inter.send('**Вы уже владеете этим каналом**', ephemeral = True)
            
        
        
            
        if inter.channel.category.id == massive[1] and inter.author.voice is None:
            await inter.response.send_message('**Вы не находитесь в голосовом канале**', ephemeral = True)
        
        else:
            pass
def setup(bot):
    bot.add_cog(voice(bot))


 
        
        
    
                
                
        
