import asyncio
import re

class IRCbot:
	def __init__(self, server, port):
		self.server = server
		self.port = port
		self.BUFF_SIZE = 4096
		self.channel = None
		self.reader = None
		self.writer = None
		self.nickname = None
	
	def make_command(self, cmd, args):
		command = cmd + ' ' + ' '.join(args) + '\r\n'
		return (command.encode())

	async def get_response(self):
		response = b''
		while (True):
			data = await self.reader.read(self.BUFF_SIZE)
			if (data.endswith(b'\r\n')):
				response += data
				break
			response += data
		return (response.decode())
	
	def get_response_code(self, response: str()) -> int():
		responses = response.split('\r\n')
		index = 0
		while (not(re.findall('\d{3,}', responses[index]))):
			index += 1
		code = responses[index].split(' ')[1]
		return (int(code))

	async def connect(self):
		self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
		return (await self.get_response())
	
	async def try_connect(self, nickname):
		self.nickname = nickname
		await self.user()
		response = await self.nick()
		print(response)
		if (self.get_response_code(response) > 400):
			raise Exception('Wrong nickname')

	async def user(self):
		self.writer.write(self.make_command('USER', [self.nickname, '0', '*', f':{self.nickname}']))
		return (await self.get_response())
	
	async def nick(self):
		self.writer.write(self.make_command('NICK', [self.nickname]))
		return (await self.get_response())

	async def join(self, channel_name):
		self.channel = channel_name
		self.writer.write(self.make_command('JOIN', [self.channel]))
		return (await self.get_response())
	
	async def privmsg(self, target, message):
		self.writer.write(self.make_command('PRIVMSG', [target, f":{message}"]))
		return (await self.get_response())

	async def disconnect(self, message = 'Goodbye'):
		self.writer.write(self.make_command('QUIT :', [message]))
		response = await self.get_response()
		self.writer.close()
		await self.writer.wait_closed()
		return (response)
