<script setup>

import GlassPanel from '../components/GlassPanel.vue'
import ProjectsList from '../components/ProjectsList.vue'

</script>

<template>
	<GlassPanel>
		<div class="main-landing-content-grid">

			<img src="/images/me.jpeg" class="me">

			<div class="description">
				<div class="short-content-container">
					<p>
						I'm Vena — a student at the City College of San Francisco and currently pursuing a dual major in Computer Engineering and Business. I love to yap about anything and everything that falls under the purview of my interests. Whether it's C++, writing short stories, or the weird things my friends get up to, let me share those stories with you :)
					</p>
				</div>
			</div>

			<ProjectsList/>
			
		</div>
	</GlassPanel>
</template>