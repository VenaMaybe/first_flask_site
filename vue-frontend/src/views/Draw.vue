<script setup>
import GlassPanel from '../components/GlassPanel.vue'

import { ref, onMounted, onBeforeUnmount } from 'vue'
import { io } from 'socket.io-client'

const canvas = ref(null)
let ctx
let drawing = false

// connect back to your Flask server; adjust the URL if needed
const socket = io('http://10.0.0.27:5000')


// resize helper
function resizeCanvas() {
	const c = canvas.value
	const { width, height } = c.getBoundingClientRect()
	// set the internal buffer to exactly match CSS size
	c.width  = width
	c.height = height
	// if you use any static config on ctx, re-apply it:
	ctx.lineWidth   = 2
	ctx.lineCap     = 'round'
	ctx.strokeStyle = '#ffffff'
}


// helper to get pointer coords relative to canvas
function getCoords(e) {
	const rect = canvas.value.getBoundingClientRect()
	// support touch events
	const clientX = e.touches ? e.touches[0].clientX : e.clientX
	const clientY = e.touches ? e.touches[0].clientY : e.clientY
	return {
		x: clientX - rect.left,
		y: clientY - rect.top
	}
}

// e is the event type being passed with event information
function startDraw(e) {
	e.preventDefault()
	drawing = true
	const { x, y } = getCoords(e)
	ctx.beginPath()
	ctx.moveTo(x, y)
}
function draw(e) {
	if (!drawing) return
	e.preventDefault()
	const { x, y } = getCoords(e)
	ctx.lineTo(x, y)
	ctx.stroke()
	socket.emit('draw_data', { x, y, endOfDraw: false})
	// broadcast to others
}
function endDraw(e) {
	if (!drawing) return
	e.preventDefault()
	drawing = false

	const { x, y } = getCoords(e)
	socket.emit('draw_data', { x, y, endOfDraw: true})
}

window.addEventListener('resize', resizeCanvas);


onMounted(() => {
	// set up canvas
	const c = canvas.value
	ctx = c.getContext('2d')
	ctx.lineWidth = 2
	ctx.lineCap = 'round'
	ctx.strokeStyle = '#ffffff'

	resizeCanvas()

	// pointer events
	c.addEventListener('mousedown', startDraw)
	c.addEventListener('mousemove', draw)
	c.addEventListener('mouseup', endDraw)
	c.addEventListener('mouseleave', endDraw)
	// for touch devices
	c.addEventListener('touchstart', startDraw)
	c.addEventListener('touchmove', draw)
	c.addEventListener('touchend', endDraw)

	// listen for remote draws
	let waitingForStart = true
	socket.on('draw_data', ({ x, y, endOfDraw}) => {
		if(endOfDraw) {
			console.log("end of draw")
			waitingForStart = true
		} else {
			if (waitingForStart) {
				ctx.beginPath()
				ctx.moveTo(x, y)
				waitingForStart = false
			} else {
				ctx.lineTo(x, y)
				ctx.stroke()
			}
		}
	})
})

onBeforeUnmount(() => {
	socket.disconnect()
})

</script>

<template>
	<GlassPanel>
		<h2>
			Welcome to the Stars!
		</h2>
		<canvas ref="canvas"></canvas>
	</GlassPanel>
</template>

<style scoped>
	h2 {
		position: absolute;
		margin: 0;
		padding: 0;
		font-weight: 400;
		font-size: 2.2em;
		line-height: 1.1;
		text-align: left;
	}
	canvas {
		inset: 0;
		position: absolute;
		box-sizing: border-box;
		height: 100%;
		width: 100%;
		touch-action: none;
	}
</style>