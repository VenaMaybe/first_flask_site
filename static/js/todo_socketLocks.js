import socket, { updateTodoList } from './todo_socket.js';
//import updateDraggableStatus from './todo_updateDraggable.js'
//import lockManager from './todo_lockManager.js';

// Listen for the 'update' event from the server
socket.on('update', function(data) {
	console.log("SOCKET UPDATE");
	updateTodoList(data.todos);
	//lockManager.updateLocks(data.locks);
	//updateDraggableStatus();
});




// Kinda trash I don't use these two anymore, delete later!!!
//socket.on('lock', function(data) {
//	lockManager.lockItem(data.todoId);
//	updateDraggableStatus();
//});
//
//socket.on('unlock', function(data) {
//	lockManager.unlockItem(data.todoId);
//	updateDraggableStatus();
//});