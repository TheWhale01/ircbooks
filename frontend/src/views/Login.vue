<template>
	<Head />
	<form v-on:submit.prevent="">
		<input type="text" name="nickname" placeholder="Nickname" v-model="nickname">
		<button type="submit" @click="try_nickname()">Connect</button>
	</form>
	<Loading v-if="showLoading" />
	<NickNameError v-if="showNickNameError" />
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
		NickNameError,
	},

	data() {
		return {
			socket: {} as Socket,
			nickname: '' as string,
			showLoading: false as boolean,
			showNickNameError: false as boolean,
		}
	},

	beforeUnmount() {
		this.socket.disconnect();
	},

	mounted() {
		this.socket = connectSocket('ws://127.0.0.1:3000/');
		this.socket.on('try_nickname', (response: boolean) => {
			if (!response) {
				this.showNickNameError = true;
				this.showLoading = false;
			}
			else
				router.push('/search');
		});
	},
	
	methods: {
		try_nickname() {
			this.showNickNameError = false;
			if (!this.nickname)
				return ;
			this.socket.emit('try_nickname', this.nickname);
			this.showLoading = true;
		}
	}
}
</script>
