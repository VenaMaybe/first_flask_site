// Establish a connection with the Socket.IO server
const socket = io();

// Lock mechanism
let lockedItems = {};

export { socket };
export { lockedItems };

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
    lockedItems = data.locks || {};
});

socket.on('lock', function(data) {
    lockedItems[data.todoId] = true;
});

socket.on('unlock', function(data) {
    delete lockedItems[data.todoId];
});