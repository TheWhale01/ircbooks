import asyncio
import uvicorn
import socketio
from irc_bot import IRCbot

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(sio)

bots = {}

def parseAuthor(line: str()):
	start = line.find(' ') + 1
	stop = line.find(' - ')
	if (start != -1 and stop != -1):
		return (line[start:stop])

def parseTitle(line: str()):
	start = line.find(' - ') + 3
	stop = line.find('.')
	if (start != -1 and stop != -1):
		return (line[start:stop])

def parseExt(line: str()):
	start = line.find('.') + 1
	stop = line.find(' ', start)
	if (start != -1 and stop != -1):
		return (line[start:stop])

def parseSize(line: str()):
	start = line.find(' ::INFO:: ') + len(' ::INFO:: ')
	stop = len(line)
	if (start != -1):
		return (line[start:stop])

def parseLine(line: str()) -> dict():
	dict = {}
	author = parseAuthor(line)
	title = parseTitle(line)
	extension = parseExt(line)
	fileSize = parseSize(line)
	if (author and title and extension and fileSize):
		dict.update({'author': author})
		dict.update({'title': title})
		dict.update({'extension': extension})
		dict.update({'fileSize': fileSize})
	dict.update({'download_line': line})
	return (dict)

@sio.event
async def connect(sid, environ):
	bots[sid] = IRCbot('irc.irchighway.net', 6669)
	print(f"Connected: {sid}")

@sio.event
async def disconnect(sid):
	await bots[sid].disconnect()
	print(f"Disconncted: {sid}")

@sio.on('try_nickname')
async def handleTryNickname(sid, data: str()):
	try:
		await bots[sid].connect()
		await bots[sid].user()
		await bots[sid].nick(data)
		await bots[sid].join("#ebooks")
	except Exception as e:
		await sio.emit('try_nickname', False, room=sid)
		await bots[sid].disconnect()
		return
	await sio.emit('try_nickname', True, room=sid)

@sio.on('searchBook')
async def handleSearchBook(sid, data: str()):
	response = None
	try:
		response = await bots[sid].search_book(data)
	except Exception as e:
		await sio.emit('searchBook', None, room=sid)
		return 
	result = []
	for line in response:
		result.append(parseLine(line))
	await sio.emit('searchBook', result, room=sid)

@sio.on('downloadBook')
async def handleDownloadBook(sid, data: str()):
	await bots[sid].download_book(data)
	await sio.emit('downloadBook', None)

if (__name__ == "__main__"):
	uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)