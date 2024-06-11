import lockManager from './todo_lockManager.js';

// Establish a connection with the Socket.IO server
const socket = io();

// Function to update the todo list in the DOM
function updateTodoList(todos) {
	const todoList = document.getElementById('todo-list');
	todoList.innerHTML = '';
	todos.forEach(todo => {
		const li = document.createElement('li');
		li.setAttribute('data-id', todo.id);
		li.innerHTML = `${todo.text} <a href="#" class="btn-remove" data-id="${todo.id}">Remove</a>`;
		todoList.appendChild(li);
	});
}

// Listen for the 'update' event from the server
socket.on('update', function(data) {
	updateTodoList(data.todos);
	lockManager.updateLocks(data.locks);
});

socket.on('lock', function(data) {
	lockManager.lockItem(data.todoId);
});

socket.on('unlock', function(data) {
	lockManager.unlockItem(data.todoId);
});

export { socket };