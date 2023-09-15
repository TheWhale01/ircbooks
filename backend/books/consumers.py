from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .irc_bot import IRCbot

class ChatConsumer(AsyncWebsocketConsumer):
	def __init__(self):
		super().__init__(self)
		self.bot = None
		self.server = 'irc.irchighway.net'
		self.port = 6669
		self.nickname = None
		self.channel = '#ebooks'

	async def connect(self):
		await self.accept()
		self.bot = IRCbot(self.server, self.port)
		await self.bot.connect()

	# async def disconnect(self, close_code):
	# 	await self.bot.disconnect()

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['data']

		event = text_data_json['event']
		if (event == 'nickname'):
			self.nickname = message
			self.bot.nickname = self.nickname
			data = {
				'event': 'nickname',
				'data': await self.bot.try_connect(self.nickname),
			}
			await self.send(text_data=json.dumps(data))
		elif (event == 'IRCconnect'):
			await self.bot.user()
			await self.bot.nick()
			await self.bot.join(self.channel)
			await self.send(text_data=json.dumps({
				'event': 'IRCconnect',
				'data': True,
			}))
		elif (event == 'search'):
			# wait for file, extract it, parse it into json
			results = await self.bot.search_book(message)
			await self.send(text_data=json.dumps({
				'event': 'search',
				'data': results,
			}))