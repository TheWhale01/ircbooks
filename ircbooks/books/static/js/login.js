var submit_btn = document.getElementById('submit_nickname')
submit_btn.addEventListener('click', (e) => {
	e.preventDefault();
	var nickname = document.getElementById('nickname_field').value;
	socket.send(JSON.stringify({
		'event': 'nickname',
		'data': nickname
	}))
});