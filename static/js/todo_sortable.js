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
		super(element, options);
		console.log("Custom sortable constructor initialized");

		// Initialize socket and drag elements map
		this.socket = socket;  // Ensure 'socket' is imported or available in this scope
		this.dragEls = new Map();

		// Save original method references and extend them
		this.extendEventHandlers(options);
	}

	extendEventHandlers(options) {
		const originalOnStart = options.onStart || (() => {});
		const originalOnEnd = options.onEnd || (() => {});

		// Extend the onStart handler
		this.options.onStart = (evt) => {
			console.log("Drag started");

			const itemId = evt.item.dataset.id;
			const parentId = evt.item.parentNode.dataset.id;
			console.log(parentId);

			// Save the dragged item and its parent node
			this.dragEls.set(evt.item, evt.item.parentNode);

			// Emit the start_drag event to the server
			this.socket.emit('start_drag', { id: itemId, parentId: parentId });

			// Call the original onStart handler
			originalOnStart(evt);
		};

		// Extend the onEnd handler
		this.options.onEnd = (evt) => {
			console.log("Drag ended");

			const itemId = evt.item.dataset.id;

			// Remove the item from the drag elements map
			this.dragEls.delete(evt.item);

			// Emit the end_drag event to the server
			this.socket.emit('end_drag', { id: itemId });

			// Call the original onEnd handler
			originalOnEnd(evt);
		};

		// Listen for updates from the server
		this.socket.on('update_dragged_elements', (data) => {
			console.log('Updated dragged elements:', data);
			this.updateDragEls(data);
		});
	}

	updateDragEls(data) {
		// Clear the existing elements before updating
		this.dragEls.clear();
		console.log('clear =====================================================')
	
		// Update the map and DOM based on data from the server
		Object.entries(data).forEach(([itemId, parentId]) => {
			const item = document.querySelector(`[data-id='${itemId}']`);
			const parent = document.querySelector(`[data-id='${parentId}']`);
			console.log('meowwww parent,', parent, 'item,', item);

			
			
			if (item && parent) {
				//console.log('item and parent exist')
				// Update the dragEls map
				this.dragEls.set(item, parent);
				// Move item to its new parent if not already there
				if (todoList.querySelector(`[data-id='${itemId}']`)) {
					console.log('todo list doesnt contain a similar item');
					todoList.appendChild(item);
				}
			}
		});
	}	
}


document.addEventListener('DOMContentLoaded', () => {
	console.log(todoList);

	if (todoList) {
		
		const draggedObjects = new Map();

		new Sortable(todoList, {
			animation: 150,
			ghostClass: 'sortable-ghost',
//			filter: '.non-draggable',  // Use a class to filter out non-draggable items
			

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

				const itemId = evt.item.dataset.id;
		//		const parentId = evt.item.parentNode.id;

				socket.emit('end_drag', { itemId: itemId })



				const idAndNewIndex = {
					itemId: itemId,
					newIndex: evt.newIndex
				}

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

//				dragged.classList.add('sortable-chosen');
//				dragged.classList.add('sortable-ghost');

				//todoList.removeChild(document.querySelector(`[data-id='${itemId}']`));
				//todoList.appendChild(draggedObjects.get(itemId));

			});

			draggedObjects.clear()
		});

	} else {
		console.error('todoList does not exist, did not make sortable instance');
		}
	});
//});
