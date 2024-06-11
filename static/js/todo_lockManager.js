let lockedItems = {};

const lockManager = {
	getLockedItems: () => lockedItems,
	updateLocks: (locks) => {
		lockedItems = locks || {};
		console.log('Locked Items: ', lockedItems)
	},
	lockItem: (todoId) => {
		lockedItems[todoId] = true;
		console.log('Locked Items: ', lockedItems)
	},
	unlockItem: (todoId) => {
		delete lockedItems[todoId];
		console.log('Locked Items: ', lockedItems)
	},
	isLocked: (todoId) => {
		console.log('Locked Items: ', lockedItems)
		return !!lockedItems[todoId];
	}
};

export default lockManager;
