import { todoList } from './todo_domExports.js';
import lockManager from './todo_lockManager.js';

export default function updateDraggableStatus() {
	console.log('UPDATED DRAGGING STATUS!!!');

	const items = todoList.children;
	for (let item of items) {
		const todoId = item.dataset.id;
		if (lockManager.isLocked(todoId)) {
			item.classList.add('non-draggable');
		} else {
			item.classList.remove('non-draggable');
		}
	}
}