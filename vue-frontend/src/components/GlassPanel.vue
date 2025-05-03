<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const THROTTLE_MS = 10_000;  // 20 seconds
const panel = ref(null) // A reference so we don't select all

let lastSheen = 0;
let timeoutId

function onMouseEnter() {
	console.log("Meowth")
	
	const now = Date.now()

	// Time limit and random check
	if (now - lastSheen > THROTTLE_MS && Math.random() < 0.5) {
		lastSheen = now
		panel.value.classList.add('sheen-active')
		
		// remove the class once the animation is done
		timeoutId = setTimeout(() => {
			panel.value?.classList.remove('sheen-active')
		}, 1200) // match the css transition-duration!!
	}
}

onMounted(() => {
	panel.value?.addEventListener('mouseenter', onMouseEnter)
})

onBeforeUnmount(() => {
	panel.value?.removeEventListener('mouseenter', onMouseEnter)
	clearTimeout(timeoutId)
})
</script>

<template>
	<div ref="panel" class="glass glass-sheen">
		<div class="glass-panel"></div>
		<div class="glass-content">
			<slot/>
		</div>
	</div>
</template>