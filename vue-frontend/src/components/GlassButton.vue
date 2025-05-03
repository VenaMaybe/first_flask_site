<template>
	<button class="glass glass-inner glass-sheen">
		<span class="glass-panel-inner"></span>
			<slot>Click me</slot>
	</button>
</template>

<script>
export default {
	name: "GlassButton"
};
</script>

<style scoped>
button.glass {
	/* reset native button styles */
	appearance: none;
	background: none;
	color: inherit;
	font: inherit;
	cursor: pointer;
	display: block;
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