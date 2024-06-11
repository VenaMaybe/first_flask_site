import { socket, lockedItems } from './todo_socket.js';

const todoList = document.getElementById('todo-list');

console.log("Dragging Initialized");

if (todoList) {
	new Sortable(todoList, {
		animation: 150, // Animation duration in ms
		ghostClass: 'sortable-ghost', // Class name for the drop placeholder
		onStart: function (evt) {
			console.log('\n\nStarted Dragging: onStart')
            const todoId = evt.item.dataset.id;
            if (lockedItems[todoId]) {
                evt.preventDefault(); // Prevent drag if item is locked
            } else {
                socket.emit('lock', { todoId: todoId });
            }
        },
		onEnd: function (evt) {
			console.log('\n\nEnded Dragging: onEnd')
			const todoId = evt.item.dataset.id;
            socket.emit('unlock', { todoId: todoId });

			var itemEl = evt.item;  // dragged HTMLElement
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