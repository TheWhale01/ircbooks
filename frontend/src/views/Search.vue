<template>
	<Head />
	<p>This is the search view.</p>
	<form v-on:submit.prevent="">
		<input type="text" placeholder="Search for a book or an author" v-model="bookName">
		<button type="submit" @click="searchBooks()">Search</button>
	</form>
	<Loading v-if="showLoading" />
	<SearchResults v-if="results" :results="results"/>
</template>
<script lang="ts">
import Head from '@/components/Head.vue';
import { getWebSocketInstance } from '@/services/websocket';
import Loading from '@/components/Loading.vue';
import SearchResults from '@/components/SearchResults.vue';
import router from '@/router';

export default {
	components: {
		Head,
		Loading,
		SearchResults,
	},

	data() {
		return {
			connected: false as boolean,
			socket: {} as WebSocket,
			showLoading: false as boolean,
			bookName: '' as string,
			results: [] as string[],
		};
	},

	mounted() {
		try {
			this.socket = getWebSocketInstance();
			this.connected = true;
		}
		catch (error: unknown) {router.push('/');}
		this.socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			if (data['event'] === 'search') {
				this.showLoading = false;
				this.results = data['data'];
			}
		}
		this.socket.onclose = () => { router.push('/'); }
	},

	unmounted() {
		if (this.connected)
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