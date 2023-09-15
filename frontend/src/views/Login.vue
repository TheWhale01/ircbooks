<template>
	<Head />
	<form v-on:submit.prevent="">
		<input type="text" name="nickname" placeholder="Nickname" v-model="nickname">
		<button type="submit" @click="try_connect()">Connect</button>
	</form>
	<Loading v-if="showLoading" />
	<NickNameError v-if="showNickNameError" />
</template>
<script lang="ts">
import Head from '@/components/Head.vue';
import Loading from '@/components/Loading.vue';
import NickNameError from '@/components/NickNameError.vue';
import router from '@/router';
import { IRCconnected, connectToWebSocket } from "@/services/websocket"

export default {
	components: {
		Head,
		Loading,
		NickNameError,
	},

	data() {
		return {
			socket: {} as WebSocket,
			nickname: '' as string,
			showLoading: false as boolean,
			showNickNameError: false as boolean,
		}
	},

	mounted() {
		this.socket = connectToWebSocket('ws://127.0.0.1:3000/ws/books/');
		this.socket.onmessage = (response) => {
			const data = JSON.parse(response.data);
			if (data['event'] === 'nickname') {
				if (!data['data']) {
					this.showNickNameError = true;
					this.nickname = '';
					return ;
				}
				IRCconnected(this.nickname);
				this.socket.send(JSON.stringify({
					'event': 'IRCconnect',
					'data': null,
				}));
			}
			else if (data['event'] === 'IRCconnect') {
				if (!data['data']) {
					this.showNickNameError = true;
					return ;
				}
				router.push('/search');
			}
		}
	},

	methods: {
		try_connect() {
			if (this.nickname === '')
				return ;
			if (this.showNickNameError)
				this.showNickNameError = false;
			this.socket.send(JSON.stringify({
				'event': 'nickname',
				'data': this.nickname,
			}));
			this.showLoading = true;
		}
	},
}
</script>