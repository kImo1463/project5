// static/network/edit.js

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', event => {
        const target = event.target;
        if (target.classList.contains('edit-button')) {
            const postId = target.dataset.postId;
            const postDiv = document.getElementById(`post-${postId}`);
            const postContent = postDiv.querySelector('.post-content');

            const textarea = document.createElement('textarea');
            textarea.value = postContent.textContent;
            textarea.className = 'edit-textarea';

            const saveButton = document.createElement('button');
            saveButton.textContent = 'Save';
            saveButton.className = 'save-button';

            // Hide the edit button
            target.style.display = 'none';

            postContent.style.display = 'none';
            postContent.insertAdjacentElement('afterend', textarea);
            textarea.insertAdjacentElement('afterend', saveButton);

            saveButton.onclick = () => {
                const newContent = textarea.value;

                fetch(`/edit_post/${postId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        content: newContent
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update the post content and remove the textarea and save button
                        postContent.textContent = newContent;
                        postContent.style.display = 'block';
                        textarea.remove();
                        saveButton.remove();

                        // Show the edit button again
                        target.style.display = 'inline';
                    } else {
                        alert('Failed to update post.');
                    }
                });
            };
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}