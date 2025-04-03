let notificationVisible = false;

function copyLink(postId) {
    const link = `/posts/${postId}`;
    const fullLink = window.location.origin + link;

    if (notificationVisible) return;

    navigator.clipboard.writeText(fullLink).then(() => {
        const notification = document.getElementById('copyNotification');

        notification.style.display = 'block';
        notification.style.opacity = 1;
        notificationVisible = true;

        setTimeout(() => {
            notification.style.opacity = 0;
        }, 1000);

        setTimeout(() => {
            notification.style.display = 'none';
            notificationVisible = false;
        }, 4000);
    }).catch(err => {
        console.error("Failed to copy: ", err);
    });
}