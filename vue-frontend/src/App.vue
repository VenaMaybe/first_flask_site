<script setup>
import { useRoute } from 'vue-router'

const route = useRoute();

</script>

<template>
	<div class="bg-layer"></div>
	<div class="main-container">
		<div class="content-container">
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
		</div>
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
