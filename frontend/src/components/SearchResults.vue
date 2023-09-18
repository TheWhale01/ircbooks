<template>
	<div class="search results">
		<ul>
			<li v-for="result in results">{{ result }}</li>
		</ul>
	</div>
</template>
<script lang="ts">
import router from '@/router';

interface Book {
	author: string;
	title: string;
	size: string;
	download_line: string;
}

export default {
	props: ['results'],

	data() {
		return {
			socket: {} as WebSocket,
			books: [] as Book[],
		}
	},

	mounted() {
		// try {this.socket = getWebSocketInstance();}
		// catch (error) {router.push('/');}
		// this.socket.onmessage = (event) => { console.log(event.data); }
		// for (let result of this.results) {
		// 	// Do not show
		// 	var startIndex = 0
		// 	var stopIndex = result.indexOf(' ');
		// 	console.log(result.substring(startIndex, stopIndex));

		// }
	},

	methods: {
		// download_book(book: Book) {}
	}
}
</script>
