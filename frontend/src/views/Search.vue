<template>
	<div class="search_view_container">
		<form v-on:submit.prevent="">
			<input type="text" placeholder="Search for a book or an author" v-model="bookName">
			<button type="submit" @click="searchBooks()">Search</button>
		</form>
		<Loading v-if="showLoading" />
		<SearchResults v-if="showResults" :results="results" />
	</div>
</template>
<script lang="ts">
import Head from '@/components/Head.vue';
import Loading from '@/components/Loading.vue';
import SearchResults from '@/components/SearchResults.vue';
import router from '@/router';
import { Socket } from 'socket.io-client';
import { getSocketInstance } from '@/services/socketio.service';

export default {
	components: {
		Head,
		Loading,
		SearchResults,
	},

	data() {
		return {
			socket: {} as Socket,
			connected: false as boolean,
			showLoading: false as boolean,
			showResults: false as boolean,
			bookName: '' as string,
			results: [] as string[],
		};
	},

	mounted() {
		try {
			this.socket = getSocketInstance();
			this.connected = true;
			this.socket.on('disconnect', () => { router.push('/'); });
			this.socket.on('searchBook', (response) => {
			this.showLoading = false;
			if (!response) {
				this.bookName = '';
				console.log("No book found.");
				return;
			}
			this.results = response;
			this.showResults = true;
		})
		}
		catch (error: unknown) { router.push('/'); }
	},

	unmounted() {
		if (this.connected)
			this.socket.disconnect();
	},

	methods: {
		searchBooks() {
			if (!this.bookName)
				return;
			this.showResults = false;
			this.socket.emit('searchBook', this.bookName);
			this.showLoading = true;
		},
	},
}
</script>
<style>
.search_view_container {
	display: flex;
	flex-direction: column;
}
</style>