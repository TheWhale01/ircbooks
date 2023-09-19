<template>
	<div class="search results">
		<ul>
			<li v-for="book in books">
				<div>
					<span>{{ book.author }}</span>
					<span>{{ book.title }}</span>
					<span>{{ book.ext }}</span>
					<span>{{ book.size }}</span>
					<button @click="download_book(book)">download</button>
				</div>
			</li>
		</ul>
		<ul>
			<li v-for="parsingError in parsingErrors">
				<div>
					<span>{{ parsingError }}</span>
					<button>download</button>
				</div>
			</li>
		</ul>
	</div>
</template>
<script lang="ts">
import router from '@/router';
import type { Socket } from 'socket.io-client';
import { getSocketInstance } from '@/services/socketio.service';

interface Book {
	author: string;
	title: string;
	size: string;
	ext: string;
	download_line: string;
}

export default {
	props: ['results'],

	data() {
		return {
			socket: {} as Socket,
			books: [] as Book[],
			parsingErrors: [] as string[],
		}
	},

	beforeUnmount() {
		this.socket.disconnect();
	},

	mounted() {
		try {this.socket = getSocketInstance();}
		catch (error) {router.push('/');}
		for (let result of this.results) {
			const author = result['author'];
			const title = result['title'];
			const size = result['fileSize'];
			const ext = result['extension'];
			if (!author || !title || !size || !ext)
				this.parsingErrors.push(result['download_line']);
			else {
				this.books.push({
					author: author,
					title: title,
					size: size,
					ext: ext,
					download_line: result['download_line'],
				});
			}
		}
	},

	methods: {
		download_book(book: Book) {
			this.socket.emit('downloadBook', book.download_line);
		}
	}
}
</script>
