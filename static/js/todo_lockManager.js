let lockedItems = {};

const lockManager = {
	getLockedItems: () => lockedItems,
	updateLocks: (locks) => {
		lockedItems = locks || {};
	},
	lockItem: (todoId) => {
		lockedItems[todoId] = true;
	},
	unlockItem: (todoId) => {
		delete lockedItems[todoId];
	},
	isLocked: (todoId) => {
		return !!lockedItems[todoId];
	}
};

export default lockManager;
