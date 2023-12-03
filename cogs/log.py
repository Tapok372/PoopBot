import disnake
from disnake.ext import commands
from disnake import Localized
import sqlite3

class log(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.db = sqlite3.connect(f'PoopBot.db')
        self.table = self.db.cursor()
        self.green = 3908957
        self.red = 15548997
        self.orange = 13930527
        self.bluepurple = 5793266
    
    
    
    @commands.slash_command(name = 'логи', description = 'команда позволяющая настроить каналы логов на сервере')
    @commands.has_permissions(administrator = True)
    async def logs(
        self,
        inter,
        logging: str = commands.Param(
            choices=["Логи Сообщений", "Логи Войсов", "Логи Игроков"],
            name=Localized('логирование',key="LOGS_NAME"),
            description=Localized('Выберите вид логирования',key="LOGS_DESCRIPTION")),
        channel: disnake.TextChannel = commands.Param(
            name=Localized('канал',key="CHANNEL_NAME"),
            description=Localized('Выберите канал в котором хотите включить или выключить автореакции',key="CHANNEL_DESCRIPTION")),
        sost: str = commands.Param(
            choices=["Подключить", "Отключить"],
            name=Localized('действие',key="SOST_NAME"),
            description=Localized('Выберите действие',key="SOST_DESCRIPTION")),
    ):
        self.table.execute("SELECT channelID FROM Logs WHERE guildID = ? and log = ?",(inter.guild.id,logging,))
        channelID = self.table.fetchone()
        if channelID is not None:
            if sost == 'Подключить':
                await inter.send('Вы уже подключили это логирование на сервере', ephemeral = True)
            if sost == 'Отключить':
                channelID = channel.id
                logging = logging
                self.table.execute('DELETE FROM Logs WHERE channelID=? and log=?', (channelID,logging))
                self.db.commit()
                await inter.send(f'Логирование {logging} удалено из канала {channel.mention}', ephemeral = True)
        if channelID is None:
            if sost == 'Подключить':
                logging = logging
                self.table.execute("INSERT INTO Logs VALUES (?, ?, ?)",(inter.guild.id, logging, channel.id,))
                self.db.commit()
                await inter.send(f'Логирование {logging} добавлено в канал {channel.mention}', ephemeral = True)
            if sost == 'Отключить':
                await inter.send(f'Логирований в канале не обнаружено', ephemeral = True)



    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logging = 'Логи Сообщений'
        avatar_url = message.author.avatar
        if avatar_url == None:
            avatar_url = 'https://media.discordapp.net/attachments/982269337727549530/982275492096901130/123123.png' 
        self.table.execute("SELECT channelID FROM Logs WHERE guildID = ? and log = ?",(message.guild.id,logging,))
        massive = self.table.fetchall()
        for i in range(len(massive)):
            inv = massive[i]
            reaction = inv[0]
            msg_log = self.bot.get_channel(reaction)

            logMsg = disnake.Embed(title = "Сообщение удалено", description = f"**Канал:** `{message.channel}`\n**Автор:** `{message.author}`\n**Сообщение:** {message.content}", colour = self.red)
            logMsg.set_thumbnail(url=f"{avatar_url}")
            try:    
                fil = await message.attachments[0].to_file()
                await msg_log.send(embed = logMsg, file=fil)
            except:
                await msg_log.send(embed = logMsg)
    
    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        logging = 'Логи Сообщений'
        avatar_url = message_after.author.avatar
        if avatar_url == None:
            avatar_url = 'https://media.discordapp.net/attachments/982269337727549530/982275492096901130/123123.png' 
        self.table.execute("SELECT channelID FROM Logs WHERE guildID = ? and log = ?",(message_after.guild.id,logging,))
        massive = self.table.fetchall()
        for i in range(len(massive)):
            inv = massive[i]
            reaction = inv[0]
            msg_log = self.bot.get_channel(reaction)
            if message_before.content != message_after.content:
                logMsg = disnake.Embed(title = "Сообщение изменено", description = f"**Автор:** `{message_before.author}`\n**Канал:** `{message_before.channel}`\n**Оригинал:** {message_before.content}\n**Изменённое:** {message_after.content}", colour = self.bluepurple)
                logMsg.set_thumbnail(url=f"{avatar_url}")
                try:
                    fil = await message_before.attachments[0].to_file()
                    await msg_log.send(embed = logMsg, file=fil)
                except:
                    await msg_log.send(embed = logMsg)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        logging = 'Логи Игроков'
        avatar_url = after.avatar
        if avatar_url == None:
            avatar_url = 'https://media.discordapp.net/attachments/982269337727549530/982275492096901130/123123.png' 
        self.table.execute("SELECT channelID FROM Logs WHERE guildID = ? and log = ?",(after.guild.id,logging,))
        massive = self.table.fetchall()
        for i in range(len(massive)):
            inv = massive[i]
            reaction = inv[0]
            msg_log = self.bot.get_channel(reaction)

            if before.nick != after.nick:

                nick = disnake.Embed(description = f'**Обновление ника**\n**Игрок:** {before.mention}\n**Старый ник:** {before.nick}\n**Новый ник:** {after.nick}', colour = self.bluepurple)
                nick.set_thumbnail(url=f"{avatar_url}")
                await msg_log.send(embed=nick)
            
            if before.roles != after.roles:
                emb = disnake.Embed(description = f'**Обновление ролей {before.mention}**', colour = self.bluepurple)
                emb.add_field(name = '**Роли до**', value = ", ".join([r.mention for r in before.roles])) 
                emb.add_field(name = '**Роли после**', value = ", ".join([r.mention for r in after.roles])) 
                emb.set_thumbnail(url=f"{avatar_url}")
                async for event in before.guild.audit_logs(limit=1, action=disnake.AuditLogAction.member_role_update): 
                    if getattr(event.target, "id", None) != before.id:
                        continue
                    emb.add_field(name="Изменённые роли", value = ", ".join([getattr(r, "mention", r.id) for r in event.before.roles or event.after.roles]))  
                    emb.add_field(name="Обновил:", value = event.user)
                    break
                await msg_log.send(embed = emb)
        
        roleBuster = before.guild.get_role(996818993962831873)
        if before.guild.id == 995379037407027270:
            if roleBuster in before.roles and roleBuster not in after.roles:
                roleCol1 = before.guild.get_role(1036328772053499994)
                roleCol2 = before.guild.get_role(1036328534727196712)
                roleCol3 = before.guild.get_role(1036328094946054155)
                roleCol4 = before.guild.get_role(1036327805115453511)
                roleCol5 = before.guild.get_role(1036327408594325735)
                roleCol6 = before.guild.get_role(1041321228432052224)
                await after.member.remove_roles(roleCol1, roleCol2, roleCol3, roleCol4, roleCol5, roleCol6)
                

    @commands.Cog.listener()
    async def on_voice_state_update(self, member,before,after):
        logging = 'Логи Войсов'
        avatar_url = member.avatar
        if avatar_url == None:
            avatar_url = 'https://media.discordapp.net/attachments/982269337727549530/982275492096901130/123123.png' 
        self.table.execute("SELECT channelID FROM Logs WHERE guildID = ? and log = ?",(member.guild.id,logging,))
        massive = self.table.fetchall()
        for i in range(len(massive)):
            inv = massive[i]
            reaction = inv[0]
            msg_log = self.bot.get_channel(reaction)

            if before.channel == None:

                s = disnake.Embed(description = f"**Игрок:** `{member}`\n**Пришел в:** `{after.channel}`", colour = self.green)
                await msg_log.send(embed = s)

            elif after.channel == None:  

                s = disnake.Embed(description = f"**Игрок:** `{member}`\n**Вышел из:**`{before.channel}`", colour = self.red)
                await msg_log.send(embed = s)

            else:
                if before.channel != after.channel:
                    s = disnake.Embed(description = f"**Игрок:** `{member}`\nПерешел из: `{before.channel}`\nВ: `{after.channel}`", colour = self.orange) 
                    await msg_log.send(embed= s)

def setup(bot):
    bot.add_cog(log(bot))
