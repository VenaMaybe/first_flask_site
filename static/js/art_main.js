document.addEventListener('DOMContentLoaded', () => {
	const canvas = document.getElementById('paintCanvas');
	const ctx = canvas.getContext('2d');
	let isDrawing = false;
	let lastX = 0;
	let lastY = 0;
	let points = [];

	// Initialize the off-screen canvas
	const offScreenCanvas = document.createElement('canvas');
	const offScreenCtx = offScreenCanvas.getContext('2d');

	function resizeCanvas() {
		// Save the current canvas content to the off-screen canvas
		const tempCanvas = document.createElement('canvas');
		const tempCtx = tempCanvas.getContext('2d');
		tempCanvas.width = offScreenCanvas.width;
		tempCanvas.height = offScreenCanvas.height;
		tempCtx.drawImage(offScreenCanvas, 0, 0);

		// Resize main and off-screen canvases to match the window
		const oldWidth = canvas.width;
		const oldHeight = canvas.height;
		const newWidth = window.innerWidth;
		const newHeight = window.innerHeight;

		offScreenCanvas.width = newWidth;
		offScreenCanvas.height = newHeight;
		canvas.width = newWidth;
		canvas.height = newHeight;

		// Calculate the new center
		const offsetX = (newWidth - oldWidth) / 2;
		const offsetY = (newHeight - oldHeight) / 2;

		// Redraw the image from the temporary canvas to the resized off-screen canvas
		offScreenCtx.drawImage(tempCanvas, offsetX, offsetY);

		// Draw the final off-screen canvas state to the main canvas
		ctx.drawImage(offScreenCanvas, 0, 0);
	}

	function startDrawing(e) {
		isDrawing = true;
		points = []; // Reset points array
		const { x, y } = getPosition(e);
		lastX = x;
		lastY = y;
		points.push({ x: lastX, y: lastY });
	}

	function stopDrawing() {
		isDrawing = false;
		points = [];
	}

	function draw(e) {
		if (!isDrawing) return;

		const { x, y } = getPosition(e);
		points.push({ x, y });
		if (points.length > 3) {
			points.shift(); // Keep only the last 4 points
		}

		drawSmoothLine();

		// Update the last positions for next move
		lastX = x;
		lastY = y;
	}

	function getPosition(e) {
		return {
			x: e.clientX || e.touches[0].clientX,
			y: e.clientY || e.touches[0].clientY
		};
	}

	function drawSmoothLine() {
		if (points.length < 2) return;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.drawImage(offScreenCanvas, 0, 0);

		ctx.beginPath();
		ctx.moveTo(points[0].x, points[0].y);

		for (let i = 1; i < points.length - 2; i++) {
			const c = (points[i].x + points[i + 1].x) / 2;
			const d = (points[i].y + points[i + 1].y) / 2;
			ctx.quadraticCurveTo(points[i].x, points[i].y, c, d);
		}

		// For the last two points
		ctx.quadraticCurveTo(
			points[points.length - 2].x,
			points[points.length - 2].y,
			points[points.length - 1].x,
			points[points.length - 1].y
		);

		ctx.strokeStyle = 'antiquewhite';
		ctx.lineWidth = 2.5;
		ctx.stroke();
		ctx.closePath();

		// Draw directly on the off-screen canvas to preserve the drawing
		offScreenCtx.clearRect(0, 0, offScreenCanvas.width, offScreenCanvas.height);
		offScreenCtx.drawImage(canvas, 0, 0);
	}

	// Event listeners for mouse
	canvas.addEventListener('mousedown', startDrawing);
	canvas.addEventListener('mouseup', stopDrawing);
	canvas.addEventListener('mousemove', draw);

	// Event listeners for touch
	canvas.addEventListener('touchstart', startDrawing, { passive: false });
	canvas.addEventListener('touchend', stopDrawing);
	canvas.addEventListener('touchmove', draw, { passive: false });

	// Handle resizing
	window.addEventListener('resize', resizeCanvas);

	// Set initial canvas size
	resizeCanvas();

	// Clear canvas button
	document.getElementById('clearCanvas').addEventListener('click', () => {
		offScreenCtx.clearRect(0, 0, offScreenCanvas.width, offScreenCanvas.height);
		ctx.clearRect(0, 0, canvas.width, canvas.height);
	});
});
