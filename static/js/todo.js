const todoList = document.getElementById('todo-list');

console.log("Dragging Initialized");

if (todoList) {
	new Sortable(todoList, {
		animation: 150, // Animation duration in ms
		ghostClass: 'sortable-ghost', // Class name for the drop placeholder
		onEnd: function (evt) {
			var itemEl = evt.item;  // dragged HTMLElement
			console.log('Dragged item:', itemEl);
			console.log('Old index:', evt.oldIndex);
			console.log('New index:', evt.newIndex);
			// Example: update order in the backend
			// fetch('/update-order', {
			//     method: 'POST',
			//     headers: {
			//         'Content-Type': 'application/json',
			//     },
			//     body: JSON.stringify({ oldIndex: evt.oldIndex, newIndex: evt.newIndex }),
			// });
		},
	});
}