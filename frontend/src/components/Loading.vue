<template>
	<div class="loading_overlay">
		<div class="loading_spinner"></div>
		<p>Loading...</p>
	</div>
</template>
<style scoped>
.loading_overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.6);
	display: flex;
	justify-content: center;
	align-items: center;
	flex-direction: column;
}

.loading_spinner {
	border: 4px solid #7f7f7f;
	border-top: 4px solid #0D7377;
	border-radius: 50%;
	width: 40px;
	height: 40px;
	animation: spin 2s linear infinite;
}

.loading_overlay p {
	font-family: 'Roboto';
	color: #7f7f7f;
	padding-top: 20px
}

@keyframes spin {
	0% {
		transform: rotate(0deg);
	}

	100% {
		transform: rotate(360deg);
	}
}</style>