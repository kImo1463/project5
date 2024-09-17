document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', event => {
        const target = event.target;
        if (target.classList.contains('like-button')) {
            const postId = target.dataset.postId;
            fetch(`/like_post/${postId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const likesCount = document.querySelector(`#likes-count-${postId}`);
                    likesCount.innerHTML = data.likes_count;
                    target.innerHTML = data.liked ? 'Unlike' : 'Like';
                }
            });
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}