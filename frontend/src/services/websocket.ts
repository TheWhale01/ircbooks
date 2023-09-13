import { ref } from "vue";

const socket = ref<WebSocket | null>(null);
var nickname: string = '';

export function connectToWebSocket(url: string): WebSocket {
	socket.value = new WebSocket(url);
	if (!socket.value)
		throw new Error('Could not instanciate websocket.');
	socket.value.onopen = () => { console.log('Connected to websocket server.'); }
	socket.value.onclose = () => { console.log('Disconnected from websocket server.'); }

	return (socket.value);
}

export function getWebSocketInstance(): WebSocket {
	if (!socket.value || !nickname)
		throw new Error('WebSocket has not been instanciated.');
	return (socket.value);
}

export function IRCconnected(name: string) {
	nickname = name;
}