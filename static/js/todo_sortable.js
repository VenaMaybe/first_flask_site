import socket from './todo_socket.js';
import { Sortable } from './Sortable.js'
import { todoList } from './todo_domExports.js'
import lockManager from './todo_lockManager.js';



console.log("Dragging Initialized");



if (todoList) {
	// Update draggable status before initializing Sortable
	// updateDraggableStatus();

	new Sortable(todoList, {
		animation: 150,
		ghostClass: 'sortable-ghost',
		filter: '.non-draggable',  // Use a class to filter out non-draggable items
		onStart: function (evt) {
			console.log('\n\nStarted Dragging: onStart');
			const todoId = evt.item.dataset.id;
			if (lockManager.isLocked(todoId)) {
				console.log('Item is locked, cannot drag.');
				evt.preventDefault(); // Prevent drag if item is locked
			} else {
				socket.emit('lock', { todoId: todoId });
				// updateDraggableStatus(); // Local Update!!
			}
		},
		onEnd: function (evt) {
			console.log('\n\nEnded Dragging: onEnd');
			const todoId = evt.item.dataset.id;
			socket.emit('unlock', { todoId: todoId });
			// updateDraggableStatus(); // Local Update!!

			var itemEl = evt.item;
			console.log('Dragged item:', itemEl);
			console.log('Old index:', evt.oldIndex);
			console.log('New index:', evt.newIndex);

			// Get the updated order of all items
			const updatedOrder = Array.from(todoList.children).map(item => item.dataset.id);
			console.log('Updated order:', updatedOrder);

			// Send the updated order to the server
			fetch('/update-order', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ order: updatedOrder }),
			}).then(response => response.json())
			  .then(data => console.log(data))
			  .catch(error => console.error('Error:', error));
		},
	});
}