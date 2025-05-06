import socket from './todo_socket.js';
import Sortable from './sortable.esm.js';
import { todoList } from './todo_domExports.js';

console.log("Dragging Initialized");

// Helper function to get an array of todo IDs from the DOM list
function getTodoIds() {
	return Array.from(todoList.children).map(item => item.dataset.id);
}

document.addEventListener('DOMContentLoaded', () => {
	console.log(todoList);

if (todoList) {
	
	const draggedObjects = new Map();

	new Sortable(todoList, {
		animation: 150,
		ghostClass: 'sortable-ghost',

		onStart: function (evt) {
			console.log('\n\nStarted Dragging: onStart');

			const item = evt.item
			const itemId = evt.item.dataset.id;
			let parentId = null;
			if(evt.item.parentNode.id) {
				parentId = evt.item.parentNode.id;
			}

			draggedObjects.set(itemId, item)
			socket.emit('start_drag', { itemId: itemId, parentId: parentId })
		},
		onEnd: function (evt) {
			console.log('\n\nEnded Dragging: onEnd');

			const itemId = evt.item.dataset.id;
			socket.emit('end_drag', { itemId: itemId })

			const idAndNewIndex = {
				itemId: itemId,
				newIndex: evt.newIndex
			}

			fetch('/todo/update-id-location', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(idAndNewIndex),
			}).then(response => response.json())
				.then(data => console.log('POST /update-id-location:', data))
				.catch(error => console.error('Error:', error));

			console.log('New Id Order:', getTodoIds())
		}
	});

	// Listen for updates from the server
	socket.on('update_dragged_elements_end', (data) => {
		console.log('Updated dragged elements end:', data);

		Object.entries(data).forEach(([itemId, parentId]) => {
			console.log(`ItemId: ${itemId}, ParentId: ${parentId}`);
			
			let dragged = "Nothing being dragged";
			if(draggedObjects.get(itemId)) {
				dragged = draggedObjects.get(itemId);
			}
			console.log('dragged:', dragged)
		});

		draggedObjects.clear()
	});

} else {
	console.error('todoList does not exist, did not make sortable instance');
	}
});
