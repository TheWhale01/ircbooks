<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Footer from './components/Footer.vue';
import Head from './components/Head.vue';
</script>

<template>
	<Head />
	<RouterLink to="/" />
	<RouterLink to="/search" />
	<RouterView />
	<Footer />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');

* {
	margin: 0;
	padding: 0;
	font-family: 'Roboto';
}

body {
	background-color: #323232;
	height: 100vh;
}
</style>
