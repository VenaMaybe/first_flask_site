<script setup>
import { ref, onMounted } from 'vue'
import GlassButton from './GlassButton.vue'

const CACHE_KEY = 'projects_cache'
const projects = ref([])

onMounted(async () => {
	// 1. hydrate from cache
	const cached = localStorage.getItem(CACHE_KEY)
	if (cached) {
		try {
			projects.value = JSON.parse(cached)
		} catch (e) {
			console.warn('Invalid cache, clearing:', e)
			localStorage.removeItem(CACHE_KEY)
		}
	}

	// 2. fetch fresh
	try {
		const res   = await fetch('/api/projects')
		if (!res.ok) throw new Error(`HTTP ${res.status}`)
		const fresh = (await res.json()).projects || []

		// 3. update only if changed
		if (JSON.stringify(fresh) !== JSON.stringify(projects.value)) {
			projects.value = fresh
			localStorage.setItem(CACHE_KEY, JSON.stringify(fresh))
		}
	} catch (err) {
		console.error('Failed to fetch projects:', err)
	}
})

function openProject(url) {
	window.open(url, '_blank')
}
</script>

<template>
	<ul>
		<li v-for="p in projects" :key="p.id">
			<GlassButton @click="openProject(p.url)">
				<h3>{{ p.name }}</h3>
				<p>{{ p.desc }}</p>
			</GlassButton>
		</li>
	</ul>
</template>
