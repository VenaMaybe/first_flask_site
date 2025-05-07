<script setup>
import { RouterView, useRoute } from 'vue-router'

const route = useRoute();

</script>

<template>
	<div class="bg-layer"></div>
	<div v-if="route.meta.fullFlex" class="full-flex-wrapper full-flex">
		<main>
			<RouterView/>
		</main>
	</div>
	<div v-else class="main-container" :class="{ 'full-flex': route.meta.fullFlex }">
		<header>
			<div class="header-top">
				<h1>
					<RouterLink to="/">Vena Maybe</RouterLink>
				</h1>
				<nav>
					<RouterLink class="a-nav" to="/about">Me</RouterLink>
					<RouterLink class="a-nav" to="/projects">Projects</RouterLink>
					<RouterLink class="a-nav" to="/posts/">Writing</RouterLink>
					<RouterLink class="a-nav" to="/resume">Resume</RouterLink>
				</nav>
			</div>
		</header>
		<hr>
		<main>
			<RouterView />
			<!-- -->
		</main>
		<hr>
		<p>
			<strong>Current route path:</strong> {{ route.fullPath }}
		</p>
	</div>
</template>

<style>
.full-flex-wrapper {
	height: 100%;
	display: flex;
	flex-direction: column;
	flex: 1;
}
</style>