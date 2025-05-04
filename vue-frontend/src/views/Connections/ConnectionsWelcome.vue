<script setup>
import { userStore } from '../../stores/user'
</script>

<template>
	<h2>
		Welcome {{ userStore.user.first }}
	</h2>
</template>