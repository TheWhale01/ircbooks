<template>
	<Head />
	<p>This is the search view.</p>
</template>
<script lang="ts">
import Head from '@/components/Head.vue';

export default {
	components: {	
		Head,
	},

	mounted() {
		console.log('bonsoir from search view.');
	}
}
</script>