<script setup>
import { userStore } from '../../stores/user'

import GlassPanel from '../../components/GlassPanel.vue'
import GlassButton from '../../components/GlassButton.vue'
</script>

<template>
	<GlassPanel>
		<header>
			<div class="header-top">

				<RouterView name="header" />

				
				<nav class="auth">
					<span v-if="userStore.loading">
						<p> …loading… </p>
					</span>
					<template v-else>
						<span v-if="userStore.user">
							<p> {{ userStore.user.name }} - <a href="/logout"> Log out </a></p>
						</span>
						<a v-else href="/login">
							<p> Log in </p>
						</a>
					</template>
					<hr class="clean">
				</nav>
				
			</div>
		</header>
		
		<RouterView/>
	</GlassPanel>
</template>

<style scoped>

.header-top .auth {
	margin-left: auto;
}

hr.clean {
	margin: 0 auto 0 -20%;
	width:  120%;
}

</style>