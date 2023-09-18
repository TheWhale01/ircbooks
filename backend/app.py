import asyncio
import uvicorn
import socketio
from irc_bot import IRCbot

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(sio)

bots = {}

@sio.event
async def connect(sid, environ):
	bots[sid] = IRCbot('irc.irchighway.net', 6669)
	await bots[sid].connect()
	print(f"Connected: {sid}")

@sio.event
async def disconnect(sid):
	await bots[sid].disconnect()
	print(f"Disconncted: {sid}")

@sio.on('try_nickname')
async def handleTryNickname(sid, data: str()):
	try:
		await bots[sid].user()
		await bots[sid].nick(data)
		await bots[sid].join("#ebooks")
	except Exception as e:
		print(e)
		await sio.emit('try_nickname', False, room=sid)
		return
	await sio.emit('try_nickname', True, room=sid)

if (__name__ == "__main__"):
	uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)