<script setup>
import GlassButton from '../../components/GlassButton.vue'

</script>

<template>
	<div class="glass-content">
		<h2>
			Please log in with your google account!
		</h2>
		<br>
		<p style="text-align: center; margin: 0 auto; font-style: italic;">
			If you haven't signed up, logging in will automatically provide you with a user account. Later we will be adding support for other accounts!
		</p>
		<hr>
		<br>
		<h2 style="text-align: left;">
			Howdy!
		</h2>
		<br>
		<p>
			Connections is a simple tool to keep track of your friends, enemies, frenemies, and the connections between them. I am making this tool so that when I leave CCSF, I will be able to remember people I met along the way!
		</p>
		<br>
		<p>
			- Vena
		</p>
	</div>
	<GlassButton>
		<RouterLink to="/">
			<h3 class="wide-button">
				Back
			</h3>
		</RouterLink>
	</GlassButton>
</template>

<style scoped>
p {
	text-align: left;
	max-width: 420px;
}

</style>