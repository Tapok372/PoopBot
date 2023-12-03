import disnake
import asyncio
from disnake.ext import commands

class Call(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.component_before = disnake.ui.ActionRow(
            disnake.ui.Button(style = disnake.ButtonStyle.green, custom_id = 'Принять Вызов', label = 'Принять')
        )

    #take_the_call отвечает за нажатие кнопки 'Принять', при нажатии срабатывает данный ивент.
    async def take_the_call(self, interaction, guild):
        nick = interaction.author.nick
        if nick is None:
            interaction.author.name
        components_after = disnake.ui.Button(style = disnake.ButtonStyle.green, custom_id = f'принял(а)', label = f'{nick} принял(а)', disabled = True)
        await interaction.message.edit(components = components_after)
        user_id = interaction.message.embeds[0].footer.text
        user = await guild.fetch_member(user_id)
        

        await interaction.response.send_message('**Вы успешно приняли вызов!**', ephemeral = True)
        await user.send(f'Ваш {interaction.message.embeds[0].title} принят `{nick}`, ожидайте.')

    @commands.Cog.listener(name = 'on_message')
    async def on_message(self, message):
        guild = self.bot.get_guild(995379037407027270)
        if message.channel.id == 1085622468955344987: #Канал вызовов в который приходят вызовы с сайта.
            content = message.content
            split_content = content.split()
            id = split_content[1][:-1][1:]
            structure = split_content[3]
            description = content.rsplit('`', 2)
            nickname = content.split('`', 2)
            user = await guild.fetch_member(id[:-1][2:])
            avatar_url = user.avatar
            struct = structure[:-1][3:]
            roleeee = guild.get_role(int(struct))
            if avatar_url == None:
                avatar_url = 'https://media.discordapp.net/attachments/780806472619261982/968208976095350835/1636180728_64-papik-pro-p-logotip-diskord-foto-67.png'

            embed = disnake.Embed(title = f'Вызов {roleeee.name}', description = f'**Никнейм:** `{nickname[1]}`\n**Пинг:** {id}\n**Место:** `{description[1]}`')
            embed.set_footer(text = id[:-1][2:])
            embed.set_thumbnail(url = avatar_url)
            channel = self.bot.get_channel(1147976856545542284) #Сюда айди канала для вызовов в int
            await channel.send(structure, embed = embed, components = self.component_before)

    @commands.Cog.listener(name = 'on_button_click')
    async def on_button_click(self, interaction):
        guild = self.bot.get_guild(995379037407027270)
        roleBank = guild.get_role(995743178965651456 )
        roleDetective = guild.get_role(995744050143580161)
        roleFBI = guild.get_role(995743116118204506)
        roleYst = guild.get_role(1023278766518194249)
        roleMZ = guild.get_role(1006932328502800434)
        structure = interaction.message.embeds[0].title
        if interaction.channel.id == 1147976856545542284:
            #if interaction.author.id == int(interaction.message.embeds[0].footer.text):
                #await interaction.send('Вы не можете принять свой вызов!', ephemeral = True)
            #else:
                if interaction.component.custom_id == 'Принять Вызов' and structure == 'Вызов Сотрудник Банка' and roleBank in interaction.author.roles:
                    await self.take_the_call(interaction = interaction, guild = guild)
                
                elif interaction.component.custom_id == 'Принять Вызов' and structure == 'Вызов Детектив' and roleDetective in interaction.author.roles:
                    await self.take_the_call(interaction = interaction, guild = guild)
                
                elif interaction.component.custom_id == 'Принять Вызов' and structure == 'Вызов Сотрудник ПД' and roleFBI in interaction.author.roles:
                    await self.take_the_call(interaction = interaction, guild = guild)
            
                elif interaction.component.custom_id == 'Принять Вызов' and structure == 'Вызов Сотрудник МЗ' and roleMZ in interaction.author.roles:
                    await self.take_the_call(interaction = interaction, guild = guild)
                
                elif interaction.component.custom_id == 'Принять Вызов' and structure == 'Вызов Сотрудник Юстиции' and roleYst in interaction.author.roles:
                    await self.take_the_call(interaction = interaction, guild = guild)
                
                else:
                    await interaction.send('Вы не можете принять этот вызов!', ephemeral = True)




def setup(bot):
    bot.add_cog(Call(bot))
