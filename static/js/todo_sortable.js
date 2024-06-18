import socket from './todo_socket.js';
import Sortable from './sortable.esm.js';
import { todoList } from './todo_domExports.js';
import lockManager from './todo_lockManager.js';

console.log("Dragging Initialized");

// Helper function to get an array of todo IDs from the DOM list
function getTodoIds() {
	return Array.from(todoList.children).map(item => item.dataset.id);
}

// Check if the array has duplicates
function hasDuplicates(array) {
	return new Set(array).size !== array.length;
}

// Function to remove all children with the same ID
function removeAllChildrenWithId(parent, id) {
	const children = Array.from(parent.children);
	children.forEach(child => {
		if (child.dataset.id === id) {
			parent.removeChild(child);
		}
	});
}

// Function to re-parent an element if needed
function reparentElement(element, parent) {
	if (!element.parentNode) {
		parent.appendChild(element);
	}
}

// Extension of the default Sortable library with custom setters
class CustomSortable extends Sortable {
	constructor(element, options) {
		// Save the original method references.
		const originalOnStart = options.onStart || (() => {});
		const originalOnEnd = options.onEnd || (() => {});

		// Extend the onStart and onEnd handlers.
		options.onStart = (evt) => {
			const todoId = evt.item.dataset.id;
			if (!this.dragEls) {
				this.dragEls = {};
			}
			this.dragEls[todoId] = evt.item; // Capture the item being dragged
			originalOnStart(evt);
		};

		options.onEnd = (evt) => {
			const todoId = evt.item.dataset.id;
			if (this.dragEls && this.dragEls[todoId]) {
				delete this.dragEls[todoId]; // Clear the dragEl on drag end
			}
			originalOnEnd(evt);
		};

		// Call the parent constructor with the modified options
		super(element, options);
	}

	setParentNode(todoId, newParentNode) {
		console.log('PLEASE WORK:', this.dragEls);
		if (this.dragEls && this.dragEls[todoId] && newParentNode) {
			newParentNode.appendChild(this.dragEls[todoId]);
			console.log('Parent node set for dragEl:', this.dragEls[todoId]);
		} else {
			console.error('Failed to set parent node for dragEl');
		}
	}
}

document.addEventListener('DOMContentLoaded', () => {
	console.log(todoList);

	if (todoList) {
		/*const sortableInstance = */new Sortable(todoList, {
			animation: 150,
			ghostClass: 'sortable-ghost',
//			filter: '.non-draggable',  // Use a class to filter out non-draggable items
			
			onStart: function (evt) {
				console.log('\n\nStarted Dragging: onStart');
//				console.log('evt.item', evt.item, 'evt.item.parent:', evt.item.parentNode);
//				const todoId = evt.item.dataset.id;

				// Set parent node during drag start
				//sortableInstance.setParentNode(todoId, todoList);

//				console.log('evt.item', evt.item, 'evt.item.parent:', evt.item.parentNode);

//				if (lockManager.isLocked(todoId)) {
//					console.log('Item is locked, cannot drag.');
//					evt.preventDefault(); // Prevent drag if item is locked
//				} else {
//					socket.emit('lock', { todoId: todoId });
//				}
			},
			onEnd: function (evt) {
				console.log('\n\nEnded Dragging: onEnd');

//				const allIds = {
//					order: getTodoIds()
//				}
//				
//				console.log('Sending POST to /update-order');
//				// Send the updated order to the server
//				fetch('/update-order', {
//					method: 'POST',
//					headers: {
//						'Content-Type': 'application/json',
//					},
//					body: JSON.stringify(allIds),
//				}).then(response => response.json())
//				  .then(data => console.log('POST /update-order:', data))
//				  .catch(error => console.error('Error:', error));
					
				const idAndNewIndex = {
					id: evt.item.dataset.id,
					newIndex: evt.newIndex
				}

				console.log('evt.newIndex:', evt.newIndex);
				console.log('evt.item.dataset.id:', evt.item.dataset.id);

				fetch('/update-id-location', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(idAndNewIndex),
				}).then(response => response.json())
				  .then(data => console.log('POST /update-id-location:', data))
				  .catch(error => console.error('Error:', error));

				console.log('New Id Order:', getTodoIds())


//				const todoId = evt.item.dataset.id;
				//sortableInstance.setParentNode(todoId, todoList);

//				socket.emit('unlock', { todoId: todoId });

				// Delay the execution to ensure Sortable has completed its DOM manipulations
//				setTimeout(() => {
//					// Check if the item exists using the helper function
//					const allIds = getTodoIds();
//					console.log('Updated order 1:', allIds);
//					console.log('Updated todoList 1:', todoList);
//
//					let fat = allIds;
//					if (hasDuplicates(allIds)) {
//						console.log("\t\tMEOW MEOW MEOW IT EXISTS IN ITEM");
//
//						// Since it already exists, move it to a new position instead of duplicating it!!
//						const newIndex = evt.newIndex;
//
//						const movedItem = evt.item;
//						console.log('Updated rats rats rats 1:', getTodoIds());
//						removeAllChildrenWithId(todoList, todoId); // Remove all to refill!!
//						console.log('Updated rats rats rats 2:', getTodoIds());
//
//						// Insert at new position
//						if (newIndex >= todoList.children.length) {
//							todoList.appendChild(movedItem); // Append to the end if newIndex is out of bounds
//						} else {
//							todoList.insertBefore(movedItem, todoList.children[newIndex]);
//						}
//
//						console.log("\t\t\t\tMEOW MEOW MEOW IT HAS BEEN REMOVED");
//						fat = getTodoIds();
//						console.log('Updated order 1.5:', fat);
//					}
//
//					reparentElement(evt.item, todoList);

//					console.log('Sending POST to /update-order');
//					// Send the updated order to the server
//					fetch('/update-order', {
//						method: 'POST',
//						headers: {
//							'Content-Type': 'application/json',
//						},
//						body: JSON.stringify({ order: fat }),
//					}).then(response => response.json())
//					  .then(data => console.log(data))
//					  .catch(error => console.error('Error:', error));


					  
//				}, 0);
//
//				const updatedIdOrder = getTodoIds();
//				console.log('Dragged item:', evt.item);
//				console.log('Old index:', evt.oldIndex);
//				console.log('New index:', evt.newIndex);
//				console.log('Updated order 2:', updatedIdOrder);
//				console.log('Updated todoList 2:', todoList);
			}
		});
	} else {
		console.error('todoList does not exist, did not make sortable instance');

//		console.log('Sortable element or its parent is not found');
//		// Optionally, add a parent or handle the error
//		// For example, append the todoList to a parent if it doesn't have one
//		if (todoList) {
//			const parent = document.createElement('div');
//			parent.id = 'sortable-parent';
//			parent.appendChild(todoList);
//			document.body.appendChild(parent);
//
//			new Sortable(todoList, {
//				// your sortable options
//			});
		}
	});
//});
