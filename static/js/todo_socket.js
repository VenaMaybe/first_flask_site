import { todoList } from './todo_domExports.js'
// Establish a connection with the Socket.IO server
const socket = window.io(); // Yoinks io() from the CDN Global Variable
export default socket;

// Function to update the todo list in the DOM
export function updateTodoList(todos) {
	Array.from(todoList.children).forEach(element => {
		if (!element.classList.contains('sortable-chosen')) {
			element.remove();
		}
	})

	//todoList.innerHTML = '';
	
	todos.forEach(todo => {
		const li = document.createElement('li');
		li.setAttribute('data-id', todo.id);
		li.innerHTML = `${todo.text} <a href="#" class="btn-remove" data-id="${todo.id}">Remove</a>`;
		todoList.appendChild(li);
	});
}