document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.getElementById('follow-button');
    if (followButton) {
        followButton.onclick = () => {
            const username = followButton.dataset.username;
            fetch(`/follow/${username}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    followButton.innerHTML = data.following ? 'Unfollow' : 'Follow';
                }
            });
        };
    }
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