// Change this to get env variables (docker)
const socket = new WebSocket('ws://127.0.0.1:8000/ws/books/');

socket.onopen = () => {
	console.log('Connected to websocket server.');
}

socket.close = () => {
	console.log('Disconnected to websocket server.');
}