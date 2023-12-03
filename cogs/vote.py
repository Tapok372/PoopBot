from typing import Optional
import disnake
from disnake.ext import commands
import json
import os

class Button_Vote(disnake.ui.View):
	def __init__(self):
		super().__init__()
		self.value = Optional[bool]

class Vote(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.select_menu = disnake.ui.ChannelSelect(custom_id = 'g_post', placeholder = "📢 Опубликовать")
		print('Модуль {} Включен'.format(self.__class__.__name__))

	def load_json(self, filename):
		with open(filename, encoding="utf-8") as infile:
			return json.load(infile)

	def write_json(self, filename, content):
		with open(filename, "w") as outfile:
			json.dump(content, outfile, ensure_ascii=True, indent=4)

	async def request(self, inter, custom_id: str, text_input: str = []):
		options = []
		for text in text_input:
			options.append(text)
		await inter.response.send_modal(title = 'Заполните', custom_id = custom_id, components = options)

	@commands.slash_command(description = 'Голосование')
	@commands.has_permissions(administrator = True)
	async def голосование(self, inter):
		components1 = disnake.ui.ActionRow(
			disnake.ui.Button(
				style = disnake.ButtonStyle.green,
				label = 'Создать Лог',
				emoji = '✳️',
				disabled = False,
				custom_id = 'g_log' 
			),
			disnake.ui.Button(
				style = disnake.ButtonStyle.red,
				label = 'Добавить Текст',
				emoji = '🔤',
				disabled = True,
				custom_id = 'g_text' 
			),
			disnake.ui.Button(
				style = disnake.ButtonStyle.red,
				label = 'Добавить Картинку',
				emoji = '🎦',
				disabled = True,
				custom_id = 'g_image' 
			)
		)
		components2 = disnake.ui.ActionRow(
			
			disnake.ui.Button(
				style = disnake.ButtonStyle.red,
				label = 'Добавить Кнопку',
				emoji = '⏺',
				disabled = True,
				custom_id = 'g_button' 
			),
			disnake.ui.Button(
				style = disnake.ButtonStyle.red,
				label = 'Закрыть Голосование',
				emoji = '⛔',
				disabled = True,
				custom_id = 'g_close' 
			)
		)
		await inter.response.defer(ephemeral = True)
		embed = disnake.Embed(title = f"Предпросмотр Голосования", description = f'', color = disnake.Colour(0x2B2D31))
		channel = self.bot.get_channel(776012673879244840)
		msg = await inter.channel.send(embed = embed)

		embed_panel = disnake.Embed(title = f"Панель Управления", description = """
**:eight_spoked_asterisk: - Создать запись голосования**
**:loudspeaker: - Опубликовать голосование**
**:abc: - Добавить/изменить текст голосования**
**:cinema: - Добавить/изменить картинку голосования**
**:record_button: - Добавить кнопку для голосования**
**:no_entry: - Удалить кнопку для голосования**
""", color = disnake.Colour(0x2B2D31))
		
		embed_panel.set_footer(text = msg.id)
		await inter.channel.send(embed = embed_panel, components = [components1,components2, self.select_menu])
		await inter.send('Панель управления отправил', ephemeral = True)

	@commands.Cog.listener()
	async def on_button_click(self, inter):
		nickname = inter.author.nick
		if nickname is None:
			nickname = inter.author.name
		id = inter.message.embeds[0].footer.text
		if inter.component.custom_id == 'g_log':
			file = open(f"golos/{inter.message.id}.json", "w+")
			file.write("{}")
			file.close()
			load = self.load_json(f'golos/{inter.message.id}.json')
			load[str(inter.message.id)] = {}
			load[str(inter.message.id)]['text'] = "Голосование"
			load[str(inter.message.id)]['image'] = None
			load[str(inter.message.id)]['message_id'] = None
			load[str(inter.message.id)]['channel_id'] = None
			load[str(inter.message.id)]['voted'] = 0
			load[str(inter.message.id)]['candidate'] = {}
			load[str(inter.message.id)]['amount'] = 0
			load['log'] = {}
			self.write_json(f'golos/{inter.message.id}.json', load)
			components1 = disnake.ui.ActionRow(
				disnake.ui.Button(
					style = disnake.ButtonStyle.red,
					label = 'Создать Лог',
					emoji = '✳️',
					disabled = True,
					custom_id = 'g_log' 
				),
				disnake.ui.Button(
					style = disnake.ButtonStyle.green,
					label = 'Добавить Текст',
					emoji = '🔤',
					disabled = False,
					custom_id = 'g_text' 
				),
				disnake.ui.Button(
					style = disnake.ButtonStyle.green,
					label = 'Добавить Картинку',
					emoji = '🎦',
					disabled = False,
					custom_id = 'g_image' 
				)
			)
			components2 = disnake.ui.ActionRow(
				disnake.ui.Button(
					style = disnake.ButtonStyle.green,
					label = 'Добавить Кнопку',
					emoji = '⏺',
					disabled = False,
					custom_id = 'g_button' 
				),
				disnake.ui.Button(
					style = disnake.ButtonStyle.green,
					label = 'Закрыть Голосование',
					emoji = '⛔',
					disabled = False,
					custom_id = 'g_close' 
				)
			)
			await inter.response.edit_message(components = [components1,components2, self.select_menu])
			await inter.send('Успешно', ephemeral = True)

		if inter.component.custom_id == 'g_text':
			text_input = [
				disnake.ui.TextInput(label = 'Ваш текст', custom_id = '1', placeholder = 'текст', required = True)
			]
			await self.request(inter, 'g_modal_text', text_input)
		
		if inter.component.custom_id == 'g_image':
			text_input = [
				disnake.ui.TextInput(label = 'Ссылка на картинку', custom_id = '1', placeholder = 'ссылка', required = True)
			]
			await self.request(inter, 'g_modal_image', text_input)
		
		if inter.component.custom_id == 'g_button':
			text_input = [
				disnake.ui.TextInput(label = 'Текст Кнопки', custom_id = '1', placeholder = 'текст', required = True)
			]
			await self.request(inter, 'g_modal_add_button', text_input)
		
		if inter.component.custom_id == 'g_close':
			load = self.load_json(f'golos/{inter.message.id}.json')
			title = load[str(inter.message.id)]['text']
			message_id = load[str(inter.message.id)]['message_id']
			channel_id = load[str(inter.message.id)]['channel_id']
			channel = self.bot.get_channel(channel_id)
			msg = await channel.fetch_message(message_id)
			voted = load[str(inter.message.id)]['voted']
			candidate = load[str(inter.message.id)]['candidate']
			amount = load[str(inter.message.id)]['amount']
			text = ''
			for i in candidate:
				candidate = i
				vote = load[str(inter.message.id)]['candidate'][i]
				proc = (vote / voted) * 100
				text += f"**{candidate}** : {vote} - {round(proc, 1)}%\n"
			embed = disnake.Embed(title = title, description = text, color = disnake.Colour(0x2B2D31))
			embed.set_footer(text = f"Проголосовало: {voted}")
			file = disnake.File(f'golos/{inter.message.id}.json', filename =f'golos/{inter.message.id}.json')
			chl = self.bot.get_channel(1004371026131562507)
			await chl.send(file=file)
			await msg.edit(embed = embed, components = None)
			await inter.send('Голосование Закрыто!', ephemeral = True)
	
		try:
			load = self.load_json(f'golos/{id}.json')
			name = load[str(id)]['candidate']	
			if inter.component.custom_id in name:
				log = load['log']
				if str(inter.author.id) in log:
						await inter.send('Вы уже голосовали', ephemeral = True)
				elif str(inter.author.id) not in log:
					load['log'][str(inter.author.id)] = {}
					load['log'][str(inter.author.id)]['name'] = nickname
					load['log'][str(inter.author.id)]['vote'] = inter.component.custom_id
					load[str(id)]['candidate'][inter.component.custom_id] += 1
					load[str(id)]['voted'] += 1
							
					self.write_json(f'golos/{id}.json', load)
					voted = load[str(id)]['voted']

					embed = disnake.Embed(title = inter.message.embeds[0].title, description = f'**Проголосовало:** {voted}', color = disnake.Colour(0x2B2D31)) 
					embed.set_footer(text = inter.message.embeds[0].footer.text)
					await inter.message.edit(embed = embed)
					await inter.send(f'Вы проголосовали за {inter.component.custom_id}', ephemeral = True)
					print(f'{inter.author.name} - Проголосовал за {inter.component.custom_id}')
		except:
			pass

	@commands.Cog.listener()
	async def on_modal_submit(self, inter):
		if inter.custom_id == 'g_modal_text':
			text = inter.text_values['1']
			load = self.load_json(f'golos/{inter.message.id}.json')
			load[str(inter.message.id)]['text'] = text
			self.write_json(f'golos/{inter.message.id}.json', load)
			image = load[str(inter.message.id)]['image']
			text = load[str(inter.message.id)]['text']
			channel = self.bot.get_channel(inter.channel.id)
			id_msg = inter.message.embeds[0].footer.text
			msg = await channel.fetch_message(id_msg)
			if image != None:
				embed = disnake.Embed(title = f"Предпросмотр Голосования", description = f'{text}', color = disnake.Colour(0x2f3136))
				embed.set_image(url=image)
				await msg.edit(embed = embed)
			else:
				embed = disnake.Embed(title = f"Предпросмотр Голосования", description = f'{text}', color = disnake.Colour(0x2f3136))
				await msg.edit(embed = embed)
			await inter.send('Успешно', ephemeral = True)
		
		if inter.custom_id == 'g_modal_image':
			image = inter.text_values['1']
			load = self.load_json(f'golos/{inter.message.id}.json')
			load[str(inter.message.id)]['image'] = image
			self.write_json(f'golos/{inter.message.id}.json', load)
			image = load[str(inter.message.id)]['image']
			text = load[str(inter.message.id)]['text']
			channel = self.bot.get_channel(inter.channel.id)
			id_msg = inter.message.embeds[0].footer.text
			msg = await channel.fetch_message(id_msg)
			if text != None:
				embed = disnake.Embed(title = f"Предпросмотр Голосования", description = f'{text}', color = disnake.Colour(0x2f3136))
				embed.set_image(url=image)
				await msg.edit(embed = embed)
			else:
				embed = disnake.Embed(title = f"Предпросмотр Голосования", description = f'', color = disnake.Colour(0x2f3136))
				embed.set_image(url=image)
				await msg.edit(embed = embed)
			await inter.send('Успешно', ephemeral = True)
		
		if inter.custom_id == 'g_modal_add_button':
			channel = self.bot.get_channel(inter.channel.id)
			id_msg = inter.message.embeds[0].footer.text
			msg = await channel.fetch_message(id_msg)
			text = inter.text_values['1']
			id_msg = inter.message.embeds[0].footer.text
			
			load = self.load_json(f'golos/{inter.message.id}.json')
			after_json = load[str(inter.message.id)]['candidate'][text] = 0
			before_amount = load[str(inter.message.id)]['amount']
			before_amount += 1
			load[str(inter.message.id)]['amount'] = before_amount
			self.write_json(f'golos/{inter.message.id}.json', load)
			candidate = load[str(inter.message.id)]['candidate']
			view = Button_Vote()
			
			for i in candidate:
				view.add_item(disnake.ui.Button(label = i, custom_id = i, disabled = True))
			await msg.edit(view = view)
			await inter.response.send_message('Кнопка добавлена!', ephemeral = True)
	
	@commands.Cog.listener()
	async def on_dropdown(self, inter):
		if inter.component.custom_id == 'g_post':
			channel = await self.bot.fetch_channel(inter.values[0])
			load = self.load_json(f'golos/{inter.message.id}.json')
			candidate = load[str(inter.message.id)]['candidate']
			
			text = load[str(inter.message.id)]['text']
			image = load[str(inter.message.id)]['image']
			if image is None:
				image = None
			embed = disnake.Embed(title = text, description = f'**Проголосовало:** 0', color = disnake.Colour(0x2B2D31))
			embed.set_footer(text = inter.message.id)
			embed.set_image(url = image)
			view = Button_Vote()

			await inter.response.defer()
			for i in candidate:
				view.add_item(disnake.ui.Button(label = i, custom_id = i))
			message = await channel.send(embed = embed, view = view)
			load[str(inter.message.id)]['message_id'] = message.id
			load[str(inter.message.id)]['channel_id'] = message.channel.id
			self.write_json(f'golos/{inter.message.id}.json', load)
			await inter.send('Голосование открыто!', ephemeral = True)

def setup(bot):
	bot.add_cog(Vote(bot))

			