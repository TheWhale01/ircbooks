import asyncio

class IRCbot:
	def __init__(self, server, port, nickname):
		self.server = server
		self.port = port
		self.nickname = nickname
		self.BUFF_SIZE = 4096
		self.channel = None
		self.reader = None
		self.writer = None
	
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
		pass

	async def connect(self):
		self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
		return (await self.get_response())
	
	async def try_connect(self):
		await self.user()
		response = await self.nick()
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

async def main():
	server = 'irc.irchighway.net'
	port = 6667
	nickname = 'whale_'
	client = IRCbot(server, port, nickname)
	print(await client.connect())
	print(await client.user())
	print(await client.nick())
	print(await client.join('#ebooks'))
	print(await client.privmsg(client.channel, '@search percy jackson'))
	print(await client.disconnect())


if (__name__ == '__main__'):
	asyncio.run(main())
