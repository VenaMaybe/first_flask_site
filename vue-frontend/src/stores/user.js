import { reactive } from 'vue'

export const userStore = reactive({
	user: null,      // will hold { name, email, picture, … }
	loading: true,   // true while we’re fetching
	async fetch() {
		this.loading = true
		const res = await fetch('/api/user')
		if (res.ok) {
			this.user = await res.json()
		} else {
			this.user = null
		}
		this.loading = false
	}
})
