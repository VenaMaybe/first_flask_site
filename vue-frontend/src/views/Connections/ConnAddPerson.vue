<script setup>
import { ref } from 'vue' // lets us create reactive variables

const name = ref('')
const email = ref('')
const birthday = ref('')
const response = ref('')

const submitForm = async () => {
	try {
		const res = await fetch('/api/people/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',  // Important to send cookies (session)
			body: JSON.stringify({
				name: name.value,
				email: email.value,
				birthday: birthday.value  // in yyyy-mm-dd
			})
		})

		const data = await res.json()

		if (!res.ok) {
			throw new Error(data.error || 'Unknown error')
		}

		response.value = `Created person with ID ${data.id}`
	} catch (err) {
		response.value = `Error: ${err.message}`
	}
}
</script>

<template>
	<hr>
	<h1>
		Add a person
	</h1>
	<form @submit.prevent="submitForm">
		<label>Name: <input v-model="name" /></label><br />
		<label>Email: <input v-model="email" type="email" /></label><br />
		<label>Birthday: <input v-model="birthday" type="date" /></label><br />
		<button type="submit">Create Person</button>
	</form>

	<p v-if="response">{{ response }}</p>
</template>
