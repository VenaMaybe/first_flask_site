<script>
export default {
	name: "GlassButton"
};
</script>

<template>
	<button class="glass glass-inner glass-sheen">
		<span class="glass-panel"></span>
		<slot>
			<p>
				Click me
			</p>
		</slot>
	</button>
</template>



<style scoped>

.glass-panel {
	backdrop-filter: blur(15px);
	background-color: rgba(255, 255, 255, 0.00);
}

button.glass {
	/* reset native button styles */
	box-sizing: border-box;
	background: none;
	color: inherit;
	font: inherit;
	cursor: pointer;
  	width: 100%;
	padding: 4px;
	margin-bottom: 10px;
}

.glass-inner {
	box-shadow: 0 0 1px 0px rgba(255,255,255,0.3);
	transition: box-shadow 1s ease-out;
}

.glass-inner:hover {
	box-shadow: 0 0 10px 5px rgba(255,255,255,0.3);
	transition: box-shadow 0.05s ease-in-out;
}

.glass-sheen::before {
	background: transparent;
	transform: none;
	transition: none;
}
</style>