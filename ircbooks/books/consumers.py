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
		self.bot = IRCbot(self.server, self.port, self.nickname)
		print(await self.bot.connect())

	async def disconnect(self, close_code):
		pass
		print(await self.bot.disconnect())

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['data']

		event = text_data_json['event']
		if (event == 'nickname'):
			try:
				self.nickname = text_data_json['data']
				await self.bot.try_connect(self.nickname)
			except Exception as e:
				print(e)
				self.nickname = None

		# await self.send(text_data=json.dumps({'data': message}))