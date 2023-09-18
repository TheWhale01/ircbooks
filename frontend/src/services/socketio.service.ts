import { io, Socket } from "socket.io-client";

let socket = null as Socket | null;

export function connectSocket(url: string): Socket {
	socket = io(url);
	socket.on('connect', () => { console.log('Connected to socketio server.'); });
	socket.on('disconnect', () => { console.log('Disconnected from socketio server.'); });
	return (socket);
}

export function getSocketInstance(): Socket {
	if (!socket)
		throw new Error("Socket has not been instanciated.");
	return (socket);
}