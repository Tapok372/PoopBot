import disnake
from disnake.ext import commands, tasks
from datetime import timedelta, datetime
import asyncio
import sqlite3
import chat_exporter
import io
from utils import message

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.timer.start()
        self.con = sqlite3.connect('moderation.db')
        self.table = self.con.cursor()
        
        
    @commands.command()
    async def server_infosss(self, ctx):
        for guild in self.bot.guilds:
            await ctx.send(guild.name)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Модерации подключен')

    @commands.slash_command()
    @commands.has_any_role(743806507614994557, 719941717280948298, 975441486801960960, 995739756581355601)
    async def say(self, 
        inter: disnake.ApplicationCommandInteraction,
        types: str = commands.Param(choices=["msg", "emb"]),
        content = None,
        title = None,
        description = None,
        footer = None,
        colour = None
    ):
        if types == "msg": 
            await inter.channel.send(content = f"{content}")
        
        if types == "emb":
            if colour == None:
                colour = 3092790
            
            if title and description is None:
                text = disnake.Embed(colour = colour)
                message.Message.footers(footer = footer, text = text)
            
            elif title is None and description is not None:
                text = disnake.Embed(description = description, colour = colour)
                message.Message.footers(footer = footer, text = text)
            
            elif title is not None and description is None:
                text = disnake.Embed(title = title, colour = colour)
                message.Message.footers(footer = footer, text = text)
            
            elif title and description is not None:
                text = disnake.Embed(title = title, description = description, colour = colour)
                message.Message.footers(footer = footer, text = text)         
            
            await inter.channel.send(embed = text)
        
    @commands.slash_command()
    async def сайт(self, inter):
        await inter.message.delete()
        site = disnake.Embed(description = '[Ссылка на сайт](https://spworlds.ru/)', colour = 3092790)
        await inter.send(embed = site, ephemeral = True)

    @commands.command()
    async def сайт(self, ctx):
        await ctx.message.delete()
        site = disnake.Embed(description = '[Ссылка на сайт](https://spworlds.ru/)', colour = 3092790)
        await ctx.send(embed = site, ephemeral = True)

    @commands.command()
    @commands.has_any_role(743806507614994557, 719941717280948298, 975441486801960960, 995739756581355601, 1116740491082481694)
    async def history(self,ctx):
        if ctx.author.id == 712718572710789200:
            await ctx.author.send('suck my ass')
        
        else:
            transcript = await chat_exporter.export(
                ctx.channel
            )

            if transcript is None:
                return
    
            transcript_file = disnake.File(
                io.BytesIO(transcript.encode()),
                filename=f"{ctx.channel.id}-PoopBot.html",
            )

            await ctx.send(file=transcript_file)

    @commands.command()
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def purg(self, ctx, limit = 1, member: disnake.Member=None):
        await ctx.message.delete()
        msg = []
        try:
            limit = int(limit)
        except:
            return await ctx.send("Введите количество сообщений для удаления")
        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Очищено {limit} сообщений", delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Очищено {limit} сообщений {member.mention}", delete_after=3)

    @commands.command()
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def m(self, ctx, member: disnake.Member, time, *, reason: str = None):
        if reason == None:
            reason = 'Причина не указана'
        if member == None:
            pass
        if time == None:
            pass
        await ctx.message.delete()
        c = self.con.cursor()
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        tempmute = int(time[:-1]) * time_convert[time[-1]]
        role = disnake.utils.get(ctx.guild.roles, name = 'Muted')
        timestamp = datetime.utcnow()
        modlog = self.bot.get_channel(1004371026131562507)
        number = None

        self.table.execute("SELECT userID FROM Mutes WHERE userID = ?",(member.id,))
        userID = self.table.fetchone()
        if userID is not None:
            if member.id == userID[0]:
                c.execute('DELETE FROM Mutes WHERE userID=?', (member.id,))
                self.con.commit()
                self.table.execute("INSERT INTO Mutes VALUES (?, ?, ?, ?)",(number, member.id, tempmute, reason,))
                self.con.commit()
        elif userID is None:
            self.table.execute("INSERT INTO Mutes VALUES (?, ?, ?, ?)",(number, member.id, tempmute, reason,))
            self.con.commit()        
        
        MuteLog = disnake.Embed(title = 'Мут', description = f'**Модератор:** {ctx.author.mention}\n**Игрок:** {member.mention}\n**Время:** {time}\n**Причина:** {reason}', colour = 9542131)
        await modlog.send(content = f'{member.mention}' , embed = MuteLog)

        DMLog = disnake.Embed(title = 'Вы получили мут', description = f'**Время:** {time}\n**Причина:** {reason}', colour = 9542131)
        DMLog.set_thumbnail(url = ctx.guild.icon.url)
        await member.send(embed = DMLog)
        await member.add_roles(role)
        await member.edit(voice_channel=None)


    @commands.command()
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def u(self, ctx, member: disnake.Member):
        await ctx.message.delete()
        self.table.execute('DELETE FROM Mutes WHERE userID=?', (member.id,))
        self.con.commit()
        modlog = self.bot.get_channel(1004371026131562507)
        role = disnake.utils.get(ctx.guild.roles, name = 'Muted')
        UMLog = disnake.Embed(title = 'Размут', description = f'**Модератор:** {ctx.author.mention}\n**Игрок:** {member.mention}', colour = 9542131)
        await member.remove_roles(role)
        await modlog.send(content = f'{member.mention}', embed = UMLog)
    
    @commands.command()
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def w(self, ctx, member: disnake.Member, reason = None):
        await ctx.message.delete()
        modlog = self.bot.get_channel(1004371026131562507)
        timestamp = datetime.utcnow()

        WLog = disnake.Embed(title = 'Варн', description = f'**Модератор:** {ctx.author.mention}\n**Игрок:** {member.mention}\n**Причина:** {reason}', colour = 9542131)
        await modlog.send(content = f'{member.mention}', embed = WLog)
        
        DMLog = disnake.Embed(title = 'Вы получили варн', description = f'**Причина:** {reason}', colour = 9542131)
        DMLog.set_thumbnail(url = ctx.guild.icon.url)
        await member.send(content = f'{member.mention}', embed = DMLog)

    @commands.command()
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def b(self,ctx, member: disnake.Member,*, reas=None):
        await ctx.message.delete()
        modlog = self.bot.get_channel(1004371026131562507)
        roleBan = disnake.utils.get(ctx.guild.roles, id = 743145652212465796)
        timestamp = datetime.utcnow()

        await member.edit(roles =[])
        await member.add_roles(roleBan)
        bMsg = disnake.Embed(title = "Бан", description = f"**Причина:** {reas}", colour = 9542131)
        await modlog.send(f"<@{member.id}>",embed=bMsg)
    
        banDM = disnake.Embed(title = "Вас забанили", description = f'**Причина:** {reas}', timestamp = timestamp, colour = 9542131)
        banDM.set_thumbnail(url = ctx.guild.icon.url)
        await member.send(embed=banDM)
    
    @commands.command()
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def ub(self,ctx, member: disnake.Member):
        roleBan = self.guild.get_role(743145652212465796)
        roleVer = self.guild.get_role(734027990165356574)
        modlog = self.bot.get_channel(1004371026131562507)

        timestamp = datetime.utcnow()
        
        await member.remove_roles(roleBan)
        await member.add_roles(roleVer)
    
        ubMsg = disnake.Embed(title = "Разбанен", colour = 9542131)
        await modlog.send(f"<@{member.id}>", embed=ubMsg)
    
        ubanDM = disnake.Embed(title = "Вас разбанили",  timestamp = timestamp,  colour = 9542131)
        ubanDM.set_thumbnail(url = ctx.guild.icon.url)
        await member.send(embed=ubanDM)
        
        await ctx.message.delete()

    @commands.slash_command(name = 'mute', description = 'Команда мута')
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def mute(
        self,
        inter,
        member: disnake.Member,
        time,
        reason
    ):
        c = self.con.cursor()
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        tempmute = int(time[:-1]) * time_convert[time[-1]]
        role = disnake.utils.get(inter.guild.roles, name = 'Muted')
        timestamp = datetime.utcnow()
        modlog = self.bot.get_channel(1004371026131562507)
        number = None
        
        await inter.send('True', ephemeral = True)
        self.table.execute("SELECT userID FROM Mutes WHERE userID = ?",(member.id,))
        userID = self.table.fetchone()
        if userID is not None:
            if member.id == userID[0]:
                c.execute('DELETE FROM Mutes WHERE userID=?', (member.id,))
                self.con.commit()
                self.table.execute("INSERT INTO Mutes VALUES (?, ?, ?, ?)",(number, member.id, tempmute, reason,))
                self.con.commit()
        elif userID is None:
            self.table.execute("INSERT INTO Mutes VALUES (?, ?, ?, ?)",(number, member.id, tempmute, reason,))
            self.con.commit()        
        
        
        
        MuteLog = disnake.Embed(title = 'Мут', description = f'**Модератор:** {inter.author.mention}\n**Игрок:** {member.mention}\n**Время:** {time}\n**Причина:** {reason}', colour = 9542131)
        await modlog.send(content = f'{member.mention}' , embed = MuteLog)

        DMLog = disnake.Embed(title = 'Вы получили мут', description = f'**Время:** {time}\n**Причина:** {reason}', colour = 9542131)
        DMLog.set_thumbnail(url = inter.guild.icon.url)
        await member.send(embed = DMLog)
        await member.add_roles(role)
        await member.edit(voice_channel=None)
    
    @commands.slash_command(description = 'Команда размута')
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def unmute(self,
        inter,
        member: disnake.Member
    ):
        self.table.execute('DELETE FROM Mutes WHERE userID=?', (member.id,))
        self.con.commit()
        await inter.send('True', ephemeral = True)
        modlog = self.bot.get_channel(1004371026131562507)
        role = disnake.utils.get(inter.guild.roles, name = 'Muted')
        UMLog = disnake.Embed(title = 'Размут', description = f'**Модератор:** {inter.author.mention}\n**Игрок:** {member.mention}', colour = 9542131)
        await member.remove_roles(role)
        await modlog.send(content = f'{member.mention}', embed = UMLog)

    @commands.slash_command(description = 'Команда варна')
    @commands.has_any_role(995739756581355601, 995743970195939369)
    async def warn(self,
        inter,
        member: disnake.Member,
        reason
    ):
        modlog = self.bot.get_channel(1004371026131562507)
        timestamp = datetime.utcnow()
        
        await inter.send('Warn vidan nax', ephemeral = True)
        WLog = disnake.Embed(title = 'Варн', description = f'**Модератор:** {inter.author.mention}\n**Игрок:** {member.mention}\n**Причина:** {reason}', colour = 9542131)
        await modlog.send(embed = WLog)
        
        DMLog = disnake.Embed(title = 'Вы получили варн', description = f'**Причина:** {reason}', timestamp = timestamp, colour = 9542131)
        DMLog.set_thumbnail(url = inter.guild.icon.url)
        await member.send(embed = DMLog)

    @tasks.loop(seconds=5.0)
    async def timer(self):
        try:
            guild = self.bot.get_guild(995379037407027270)
            role = guild.get_role(995768784012967946)
            c = self.con.cursor()
            c.execute("SELECT number, time, userID FROM Mutes")
            massive = c.fetchall()
            for i in range(len(massive)):
                inv = massive[i]
                number = inv[0]
                time = inv[1]
                member = inv[2]
                if time >= 0:
                    ntime = time - 5
                    self.table.execute('UPDATE Mutes SET time = ? WHERE number = ?', (ntime,number,))
                    self.con.commit()
                if time <= 0:
                    
                    user = await guild.fetch_member(member)
                    await user.remove_roles(role)
                    self.table.execute('DELETE FROM Mutes WHERE number=?', (number,))
                    self.con.commit()
                
                self.con.commit()
        except:
            pass
                



        self.con.commit()

def setup(bot):
    bot.add_cog(Moderation(bot))
