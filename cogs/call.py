import disnake
from disnake.ext import commands


class call(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.green = 3908957
        self.red = 15548997
        self.orange = 13930527
        self.bluepurple = 5793266
        self.button = disnake.ui.Button(
            style = disnake.ButtonStyle.green,
            label = 'Принять вызов',
            custom_id = 'call1'
        )
    
    @commands.slash_command(name = 'куртизанка', description = 'Команда для вызова куртизанки')
    async def куртизанка(
        self,
        inter,
        times: str = commands.Param(
            name = 'время',
            description = 'Укажите время к которому куртизанка должна подъехать на место'
        ),
        locate: str = commands.Param(
            name = 'локация',
            description = 'Укажите локацию, в которую нужно приехать'
        )
    ):
        nickname = inter.author.nick
        if nickname == None:
            nickname = inter.author.name
        
        avatar_url = inter.author.avatar.url
        if avatar_url == None:
            avatar_url = 'https://media.discordapp.net/attachments/982269337727549530/982275492096901130/123123.png' 

        embed = disnake.Embed(title = 'Вызов', description = f'**{nickname}** вызвал куртизанку\n**Время:** {times}\n**Локация:** {locate}', colour = self.bluepurple)
        embed.set_thumbnail(url = avatar_url)
        embed.set_footer(text = f'ID: {inter.author.id}')
        chl = self.bot.get_channel(1040352964889546812)
        await inter.send('Вы сделали вызов Куртизанки. Когда его примут, бот отпишет вам в лс.', ephemeral = True)
        await chl.send(f'<@&1040353296147288165>',embed = embed, components = self.button)
    
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        button = disnake.ui.Button(
            style = disnake.ButtonStyle.red,
            label = f'{inter.author} принял(а)',
            custom_id = 'call2',
            disabled = True
        )
    
        if inter.component.custom_id == 'call1':
            id = inter.message.embeds[0].footer.text[4:]
            member = await inter.guild.fetch_member(id)
            await inter.message.edit(components = button)
            await member.send(f'Куртизанка {member} приняла ваш вызов, ожидайте')
            await inter.send('Вы успешно приняли вызов!', ephemeral = True)

def setup(bot):
    bot.add_cog(call(bot))