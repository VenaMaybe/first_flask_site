<script setup>
import GlassButton from './GlassButton.vue'

</script>

<template>
	<ul>
		<li>
			<GlassButton>
				<RouterLink to="/connections">
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
