let notificationVisible = false;

function copyText(textToCopy) {
    if (notificationVisible) return;

    navigator.clipboard.writeText(textToCopy).then(() => {
        const notification = document.getElementById('copyNotification');

        if (!notification) return;

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
        console.error("Failed to copy:", err);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.copyable-heading').forEach(heading => {
        heading.addEventListener('click', () => {
            const text = heading.getAttribute('data-copy-text');
            if (text) copyText(text);
        });
    });
});
