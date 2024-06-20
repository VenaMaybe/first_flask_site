import { todoList } from './todo_domExports.js'
// Establish a connection with the Socket.IO server
const socket = window.io(); // Yoinks io() from the CDN Global Variable
export default socket;

// Function to update the todo list in the DOM
export function updateTodoList(todos) {
	const existingItems = Array.from(todoList.children);
	const todoIds = todos.map(todo => todo.id);

	// Remove items that are no longer in the todos array
	console.log(todoIds);
	existingItems.forEach(item => {
		const itemId = parseInt(item.getAttribute('data-id'));
//		console.log('itemId:', itemId);
//		console.log(todoIds.includes(itemId))
		if (!todoIds.includes(itemId) && !item.classList.contains('sortable-chosen')) {
//			console.log('Removing:', item);
			item.remove();
		}
	});

	// Update existing items and add new items
	todos.forEach(todo => {
		let item = todoList.querySelector(`[data-id="${todo.id}"]`);
		console.log('item:', item);

		if (item) {
			// Update existing item if needed
			const itemContent = `${todo.text} <button href="#" class="btn-remove" data-id="${todo.id}">Remove</button>`;
			if (item.innerHTML !== itemContent) {
				item.innerHTML = itemContent;
			}
		} else {
			// Add new item
			item = document.createElement('li');
			item.setAttribute('data-id', todo.id);
			item.innerHTML = `${todo.text} <button href="#" class="btn-remove" data-id="${todo.id}">Remove</button>`;
		}

		// Append in new order!
		todoList.appendChild(item);
	});
}