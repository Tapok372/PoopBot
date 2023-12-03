import disnake

from text_rules import *
from disnake.ext import commands

class rules(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.component_one = disnake.ui.ActionRow(
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Сервера", emoji ="📗"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Информация Сервер", emoji ="📘"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Discord", emoji ="<:5464discordnew:1081895368620519495>"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Ферм", emoji ="🏭"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Нижнего Мира", emoji ="🔥")
        ) 
        self.component_two = disnake.ui.ActionRow(
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила МинЗдрава", emoji ="🧑🏿‍🦽"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Территорий", emoji ="🏙️"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Штрафы PoopLand", emoji ="💵"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Спавна", emoji ="🌄"),
        )
        
        self.component_three = disnake.ui.ActionRow(
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Энда", emoji ="🔮"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Баны", emoji ="☠️"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила Tорговли", emoji ="🛒")
        )

        self.component_court_one = disnake.ui.ActionRow(
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Как подать дело в суд?", emoji ="📜"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Правила суда", emoji ="⚖️"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Писари и Присяжные", emoji ="💼"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Права судейства и участников суда", emoji ="⚖️"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Неявки", emoji ="📨")
        )
        self.component_court_two = disnake.ui.ActionRow(
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Издержки", emoji ="🪙"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Адвокаты и Прокуроры", emoji ="💼"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "РП суды", emoji ="⚖️"),
            disnake.ui.Button(style = disnake.ButtonStyle.gray, custom_id = "Штрафы Суд", emoji ="💵"),
        )
    @commands.slash_command(name = 'правила', description = 'Команда вызывающая панель с правилами сервера')
    async def rules(self, inter):
        
        embed_one = disnake.Embed(title = DashBoardRules.title, description = DashBoardRules.description, colour = 3092790)
        embed_two = disnake.Embed(title = DashBoardCourtRules.title, description = DashBoardCourtRules.description, colour = 3092790)
        await inter.channel.send(embed = embed_one, components = [self.component_one, self.component_two, self.component_three])
        await inter.channel.send(embed = embed_two, components = [self.component_court_one, self.component_court_two])
        await inter.response.send_message('Правила залиты', ephemeral = True)


    
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id == 'Правила Сервера':
            server_tech_rules = disnake.Embed(title = ServerTechRules.title, description = ServerTechRules.description, colour = 3092790)
            server_game_rules = disnake.Embed(title = ServerGameRules.title, description = ServerGameRules.description, colour = 3092790)
            server_cheat_rules = disnake.Embed(title = CheatModsRules.title, description = CheatModsRules. description, colour = 3092790)
            await inter.response.send_message(embeds = [server_tech_rules, server_game_rules, server_cheat_rules], ephemeral = True)
        
        if inter.component.custom_id == 'Информация Сервер':
            server_information = disnake.Embed(title = ServerInfo.title, description = ServerInfo.description, colour = 3092790)
            await inter.response.send_message(embed = server_information, ephemeral = True)
        
        if inter.component.custom_id == 'Правила Discord':
            discord_rules = disnake.Embed(title = DiscordRules.title, description = DiscordRules.description, colour = 3092790)
            await inter.response.send_message(embed = discord_rules, ephemeral = True)
        
        if inter.component.custom_id == 'Правила Ферм':
            farm_rules = disnake.Embed(title = FarmRules.title, description = FarmRules.description, colour = 3092790)
            await inter.response.send_message(embed = farm_rules, ephemeral = True)

        if inter.component.custom_id == 'Правила ПД':
            police_deportament_rules = disnake.Embed(title = PoliceDeportamentRules.title, description = PoliceDeportamentRules.description, colour = 3092790)
            await inter.response.send_message(embed = police_deportament_rules, ephemeral = True)

        if inter.component.custom_id == 'Правила Нижнего Мира':
            nether_rules = disnake.Embed(title = NetherRules.title, description = NetherRules.description, colour = 3092790)
            await inter.response.send_message(embed = nether_rules, ephemeral = True)
        
        if inter.component.custom_id == 'Правила Спавна':
            spawn_rules = disnake.Embed(title = SpawnRules.title, description = SpawnRules.description, colour = 3092790)
            await inter.response.send_message(embed = spawn_rules, ephemeral = True)

        if inter.component.custom_id == 'Правила Энда':
            end_rules = disnake.Embed(title = EndRules.title, description = EndRules.description, colour = 3092790)
            await inter.response.send_message(embed = end_rules, ephemeral = True)

        if inter.component.custom_id == 'Налоги PoopLand':
            nalog_rules = disnake.Embed(title = NalogRule.title, description = NalogRule.description, colour = 3092790)
            await inter.response.send_message(embed = nalog_rules, ephemeral = True)

        if inter.component.custom_id == 'Правила МинЗдрава':
            mz_rules = disnake.Embed(title = MZRules.title, description = MZRules.description, colour = 3092790)
            await inter.response.send_message(embed = mz_rules, ephemeral = True)

        if inter.component.custom_id == 'Правила Территорий':
            territory_rules = disnake.Embed(title = TerritoriesRules.title, description = TerritoriesRules.description, colour = 3092790)
            await inter.response.send_message(embed = territory_rules, ephemeral = True)

        if inter.component.custom_id == 'Штрафы PoopLand':
            invoice_rules = disnake.Embed(title = InvoiceRules.title, description = InvoiceRules.description, colour = 3092790)
            await inter.response.send_message(embed = invoice_rules, ephemeral = True)

        if inter.component.custom_id == 'Правила Tорговли':
            trade_rules = disnake.Embed(title = TradeRules.title, description = TradeRules.description, colour = 3092790)
            await inter.response.send_message(embed = trade_rules, ephemeral = True)

        if inter.component.custom_id == 'Как подать дело в суд?':
            how_file_lawsuit = disnake.Embed(title = HowFileLawsuit.title, description = HowFileLawsuit.desciption, colour = 3092790)
            await inter.response.send_message(embed = how_file_lawsuit, ephemeral = True)

        if inter.component.custom_id == 'Баны':
            ban_rules = disnake.Embed(title = BanRules.title, description = BanRules.desciption, colour = 3092790)
            await inter.response.send_message(embed = ban_rules, ephemeral = True)

        if inter.component.custom_id == 'Правила суда':
            courl_rules = disnake.Embed(title = CourtRules.title, description = CourtRules.description, colour = 3092790)
            await inter.response.send_message(embed = courl_rules, ephemeral = True)

        if inter.component.custom_id == 'Писари и Присяжные':
            clerks_and_jurors = disnake.Embed(title = ClerksAndJurors.title, description = ClerksAndJurors.description, colour = 3092790)
            await inter.response.send_message(embed = clerks_and_jurors, ephemeral = True)

        if inter.component.custom_id == 'Права судейства и участников суда':
            rights_court = disnake.Embed(title = RightsCourt.title, description = RightsCourt.description, colour = 3092790)
            await inter.response.send_message(embed = rights_court, ephemeral = True)

        if inter.component.custom_id == 'Неявки':
            absences = disnake.Embed(title = Absences.title, description = Absences.description, colour = 3092790)
            await inter.response.send_message(embed = absences, ephemeral = True)

        if inter.component.custom_id == 'Издержки':
            costs = disnake.Embed(title = Costs.title, description = Costs.description, colour = 3092790)
            await inter.response.send_message(embed = costs, ephemeral = True)
        
        if inter.component.custom_id == 'Штрафы Суд':
            penalties = disnake.Embed(title = Penalties.title, description = Penalties.description, colour = 3092790)
            await inter.response.send_message(embed = penalties, ephemeral = True)  
        
        if inter.component.custom_id == 'Адвокаты и Прокуроры':
            lawyers_and_prosecutors = disnake.Embed(title = LawyersAndProsecutors.title, description = LawyersAndProsecutors.description, colour = 3092790)
            await inter.response.send_message(embed = lawyers_and_prosecutors, ephemeral = True) 
        
        if inter.component.custom_id == 'РП суды':
            role_play_court = disnake.Embed(title = RolePlayCourt.title, description = RolePlayCourt.description, colour = 3092790)
            await inter.response.send_message(embed = role_play_court, ephemeral = True)

def setup(bot):
    bot.add_cog(rules(bot))
