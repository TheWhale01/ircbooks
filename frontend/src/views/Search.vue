<template>
	<Head />
	<p>This is the search view.</p>
	<form v-on:submit.prevent="searchBooks">
		<input type="text" placeholder="Search for a book or an author" v-model="bookName">
		<button type="submit" @click="searchBooks()">Search</button>
	</form>
	<Loading v-if="showLoading" />
</template>
<script lang="ts">
import Head from '@/components/Head.vue';
import { getWebSocketInstance } from '@/services/websocket';
import router from '@/router';
import Loading from '@/components/Loading.vue';

export default {
	components: {
		Head,
		Loading,
	},

	data() {
		return {
			socket: {} as WebSocket,
			showLoading: false as boolean,
			bookName: '' as string,
		};
	},

	mounted() {
		try {
			this.socket = getWebSocketInstance();
			this.socket.send(JSON.stringify({
				'event': 'IRCconnect',
				'data': null,
			}));
		}
		catch { router.push('/'); }
		this.socket.onmessage = (response) => {
			const data = JSON.parse(response.data);
			console.log(data);
			if (data['event'] === 'IRCconnect')
				console.log(data['data']);
			else if (data['event'] === 'search')
				this.showLoading = false;
		}
	},

	unmounted() {
		this.socket.close();
	},

	methods: {
		searchBooks() {
			if (!this.bookName)
				return;
			this.socket.send(JSON.stringify({
				'event': 'search',
				'data': this.bookName,
			}));
			this.showLoading = true;
		},
	},
}
</script>