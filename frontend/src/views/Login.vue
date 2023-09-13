<template>
	<Head />
	<form v-on:submit.prevent="try_connect">
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
		this.socket = new WebSocket('ws://127.0.0.1:3000/ws/books/');
		this.socket.onopen = () => { console.log('connected to websocket server.'); }
		this.socket.onclose = () => { console.log('disconnected from websocket server.'); }
		this.socket.onmessage = (response) => {
			const data = JSON.parse(response.data);
			if (data['event'] === 'nickname') {
				this.showLoading = false;
				if (!data['data']) {
					this.showNickNameError = true;
					this.nickname = '';
					return ;
				}
				console.log("Good nickname: " + this.nickname);
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