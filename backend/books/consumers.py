from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .irc_bot import IRCbot

class ChatConsumer(AsyncWebsocketConsumer):
	def __init__(self):
		super().__init__(self)
		self.bot = None
		self.server = 'irc.irchighway.net'
		self.port = 6667
		self.nickname = None
		self.channel = '#ebooks'

	async def connect(self):
		await self.accept()
		self.bot = IRCbot(self.server, self.port)

	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['data']

		await self.bot.connect()
		event = text_data_json['event']
		if (event == 'nickname'):
			data = {'event': 'nickname'}
			try:
				self.nickname = text_data_json['data']
				await self.bot.try_connect(self.nickname)
				data.update({'data': self.nickname})
			except Exception as e:
				self.nickname = None
				data.update({'data': None})
			await self.bot.disconnect()
			await self.send(text_data=json.dumps(data))
		elif (event == 'IRCconnect'):
			data = {'event': 'IRCconnect'}
			try:
				await self.bot.user()
				await self.bot.nick()
				await self.bot.join(self.channel)
				data.update({'data': True})
			except Exception as e:
				data.update({'data': False})
			self.send(text_data=json.dumps(data))
		elif (event == 'search'):
			# wait for file, extract it, parse it into json
			await self.send(text_data=json.dumps({
				'event': 'search',
				'data': True,
			}))