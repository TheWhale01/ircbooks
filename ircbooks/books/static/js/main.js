// Change this to get env variables (docker)
const socket = new WebSocket('ws://127.0.0.1:8000/ws/books/');

function eventNickname(data) {
	if (!data) {
		var form_error = document.getElementsByClassName('form_error');
		form_error[0].style.display = 'block';
		return ;
	}
	// redirect to the search view
}

socket.onopen = () => {
	console.log('Connected to websocket server.');
}

socket.onmessage = (e) => {
	data = JSON.parse(e.data);
	if (data['event'] === 'nickname')
		eventNickname(data['data']);
}

socket.close = () => {
	console.log('Disconnected to websocket server.');
}