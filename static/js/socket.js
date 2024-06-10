// Establish a connection with the Socket.IO server
const socket = io();

// Function to update the todo list in the DOM
function updateTodoList(todos) {
    const todoList = document.getElementById('todo-list');
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.setAttribute('data-id', todo.id);
        li.innerHTML = `${todo.text} <a href="/remove/${todo.id}" class="btn-remove">Remove</a>`;
        todoList.appendChild(li);
    });
}

// Listen for the 'update' event from the server
socket.on('update', function(data) {
    updateTodoList(data.todos);
});