document.addEventListener('DOMContentLoaded', (event) => {
	var canvas = document.getElementById('paintCanvas');
	var ctx = canvas.getContext('2d');
	var isDrawing = false;

	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;

	canvas.addEventListener('mousedown', function(e) {
		if (e.button === 0 /*&& !isOverButton(e)*/) {
			isDrawing = true;
		}
	});

	canvas.addEventListener('mouseup', function(e) {
		if (e.button === 0) {
			isDrawing = false;
		}
	});

	canvas.addEventListener('mousemove', function(e) {
		if (isDrawing /*&& !isOverButton(e)*/) {
			drawDot(ctx, e.pageX, e.pageY);
		}
	});

	function drawDot(ctx, x, y) {
		ctx.fillStyle = 'antiquewhite';
		ctx.beginPath();
		ctx.arc(x, y, 2.5, 0, 2 * Math.PI);
		ctx.fill();
	}

	document.getElementById('clearCanvas').addEventListener('click', function() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
	});
});