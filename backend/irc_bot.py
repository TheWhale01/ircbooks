import asyncio
import re
import zipfile
import os

class IRCbot:
	def __init__(self, server, port):
		self.__server = server
		self.__port = port
		self.__BUFF_SIZE = 4096
		self.__channel = None
		self.__reader = None
		self.__writer = None
		self.__nickname = None
		self.__search_history_path = './static/search_history'
		self.__downloaded_book_path = './static/downloaded'
		self.__create_download_dirs()
	
	def __create_download_dirs(self):
		if (not os.path.exists(self.__downloaded_book_path)):
			os.makedirs(self.__downloaded_book_path)
		if (not os.path.exists(self.__search_history_path)):
			os.makedirs(self.__search_history_path)
	
	def __make_command(self, cmd, args):
		command = cmd + ' ' + ' '.join(args) + '\r\n'
		return (command.encode())

	async def __get_response(self):
		response = b''
		while (True):
			data = await self.__reader.read(self.__BUFF_SIZE)
			if (data.endswith(b'\r\n')):
				response += data
				break
			response += data
		return (response.decode())
	
	def __get_response_code(self, response: str()) -> int():
		responses = response.split('\r\n')
		index = 0
		while (not(re.findall('\d{3,}', responses[index]))):
			index += 1
		code = responses[index].split(' ')[1]
		return (int(code))

	async def connect(self):
		self.__reader, self.__writer = await asyncio.open_connection(self.__server, self.__port)
		return (await self.__get_response())

	async def user(self):
		self.__writer.write(self.__make_command('USER', ['IRCbot'] * 4))
		return (await self.__get_response())
	
	async def nick(self, nickname):
		self.__writer.write(self.__make_command('NICK', [nickname]))
		response = await self.__get_response()
		if (self.__get_response_code(response) > 400):
			raise Exception('Wrong nickname')
		self.__nickname = nickname
		return (response)

	async def join(self, channel_name):
		self.__channel = channel_name
		self.__writer.write(self.__make_command('JOIN', [self.__channel]))
		return (await self.__get_response())
	
	async def privmsg(self, message):
		if (not self.__channel):
			raise Exception('channel not joined.')
		self.__writer.write(self.__make_command('PRIVMSG', [self.__channel, f":{message}"]))
		return (await self.__get_response())

	async def disconnect(self):
		self.__writer.close()
		await self.__writer.wait_closed()
	
	async def search_book(self, book_name):
		response = await self.privmsg(f'@search {book_name}')
		while ("DCC SEND" not in response):
			response = await self.__get_response()
		args = response.split(':')[2]
		args = args.split(' ')
		filename = os.path.join(self.__search_history_path, args[2])
		ip_addr = args[3]
		port = int(args[4])
		file_size = int(args[5].replace('\x01\r\n', ''))
		filename = await self.download_file(filename, ip_addr, port, file_size)
		results = []
		with open(filename, 'r') as file:
			while (True):
				line = file.readline()
				if (not line):
					break
				if (line[0] == '!'):
					results.append(line)
		return (results)

	async def download_file(self, filename, ip_addr, __port, file_size):
		rd, wr = await asyncio.open_connection(ip_addr, __port)
		with open(filename, 'wb') as file:
			bytes = 0
			while (bytes < file_size):
				data = await rd.read(self.__BUFF_SIZE)
				if (not data):
					break
				bytes += len(data)
				file.write(data)
		wr.close()
		await wr.wait_closed()
		if (filename.endswith('.zip')):
			with zipfile.ZipFile(filename, 'r') as file:
				file.extractall(self.__search_history_path)
				filename_back = filename
				filename = os.path.join(self.__search_history_path, file.namelist()[0])
			os.remove(filename_back)
		return (filename)

async def main():
	bot = IRCbot('irc.irchighway.net', 6669)
	await bot.connect()
	print(await bot.user())
	print(await bot.nick('whale01'))
	print(await bot.join('#ebooks'))
	# print(await bot.search_book('percy jackson'))
	print(await bot.disconnect())

if (__name__ == "__main__"):
	asyncio.run(main())
