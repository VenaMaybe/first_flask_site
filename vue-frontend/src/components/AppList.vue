<script setup>
import GlassButton from './GlassButton.vue'
import { userStore } from '../stores/user';
</script>

<template>
	<ul>
		<li>
			<GlassButton>
				<RouterLink :to="userStore.user ? 
						'/connections' : '/connections/login'">
					<h3 class="wide-button">
						Connections
					</h3>
				</RouterLink>
			</GlassButton>
		</li>
		<li>
			<GlassButton>
				<RouterLink to="/draw">
					<h3 class="wide-button">
						Draw
					</h3>
				</RouterLink>
			</GlassButton>
		</li>
	</ul>
</template>
