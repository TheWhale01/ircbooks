<template>
	<div class="login_container">
		<form v-on:submit.prevent="">
			<h2>Login</h2>
			<div>
				<input type="text" name="nickname" placeholder="Nickname" autocomplete="off" v-model="nickname">
				<NickNameError v-if="showNickNameError" />
			</div>
			<button type="submit" @click="try_nickname()">Connect</button>
		</form>
		<Loading v-if="showLoading" />
	</div>
</template>
<script lang="ts">
import Head from '@/components/Head.vue';
import Loading from '@/components/Loading.vue';
import NickNameError from '@/components/NickNameError.vue';
import { Socket } from 'socket.io-client';
import { connectSocket } from '@/services/socketio.service';
import router from '@/router';

export default {
	components: {
		Head,
		Loading,
		NickNameError
	},

	data() {
		return {
			disconnect: true as boolean,
			socket: {} as Socket,
			nickname: '' as string,
			showLoading: false as boolean,
			showNickNameError: false as boolean,
		}
	},

	beforeUnmount() {
		if (this.disconnect)
			this.socket.disconnect();
	},

	mounted() {
		this.socket = connectSocket('ws://127.0.0.1:3000/');
		this.socket.on('try_nickname', (response: boolean) => {
			if (!response) {
				this.showNickNameError = true;
				this.showLoading = false;
				return;
			}
			this.disconnect = false;
			router.push('/search');
		});
	},

	methods: {
		try_nickname() {
			this.showNickNameError = false;
			if (!this.nickname)
				return;
			this.socket.emit('try_nickname', this.nickname);
			this.showLoading = true;
		}
	}
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');
.login_container {
	width: 100%;
	height: 80vh;
	display: flex;
	justify-content: center;
	align-items: center;
}

.login_container form {
	display: flex;
	flex-direction: column;
	width: 20%;
	height: 35%;
	align-items: center;
	justify-content: space-between;
	background-color: #212121;
	box-shadow: 1px 1px 2px #212121;
	padding: 15px 15px 15px 15px;
}

.login_container form h2 {
	font-family: 'Roboto';
	color: #F7F7FF;
	width: 100%;
}

.login_container form div { width: 100%; }

.login_container form input {
	background-color: transparent;
	border: none;
	border-bottom: 1px solid #F7F7FF;
	color: #F7F7FF;
	padding: 5px 5px 5px 5px;
	margin-bottom: 10px;
	width: 100%;
	font-size: large;
	font-family: 'Roboto';
}

.login_container form input:focus {
	outline: none;
}

.login_container form button {
	width: 40%;
	height: 40px;
	font-family: 'Roboto';
	color: #212121;
	background-color: #14FFEC;
	border: none;
	border-radius: 20px;
	cursor: pointer;
}
</style>