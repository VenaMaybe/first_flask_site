document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission for adding a new todo
    document.querySelector('#add-todo-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const input = document.querySelector('.input-todo');
        const todoText = input.value;

        fetch('/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `todo=${encodeURIComponent(todoText)}`,
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                input.value = '';  // Clear the input field
            }
        });
    });

    // Handle click event for removing a todo
    document.getElementById('todo-list').addEventListener('click', function(event) {
        event.preventDefault();

        // Determine the correct element from which to retrieve `data-id`
        let targetElement = event.target;
        while (targetElement != null && !targetElement.hasAttribute('data-id')) {
            targetElement = targetElement.parentElement;
        }

        if (targetElement && targetElement.classList.contains('btn-remove')) {
            const todoId = targetElement.getAttribute('data-id');

            if (todoId) {
                fetch(`/remove/${todoId}`, {
                    method: 'POST',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        console.log('Item removed successfully');
                    } else {
                        console.error('Failed to remove item:', data);
                    }
                })
                .catch(error => console.error('Error removing item:', error));
            } else {
                console.error('No todo ID found on element:', targetElement);
            }
        }
    });
});
