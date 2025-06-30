let notificationTimeout;

function showNotification() {
    const notification = document.getElementById('copyNotification');

    // Si une précédente animation est en cours, on l'annule
    clearTimeout(notificationTimeout);

    // Réinitialise l'affichage
    notification.style.display = 'block';
    notification.style.opacity = 1;

    // Lance un nouveau timeout pour masquer la notification
    notificationTimeout = setTimeout(() => {
        notification.style.opacity = 0;
        setTimeout(() => {
            notification.style.display = 'none';
        }, 500);
    }, 2000);
}

document.querySelectorAll('.copyable-heading').forEach(h1 => {
    h1.addEventListener('click', () => {
        const textToCopy = h1.getAttribute('data-copy-text');
        if (!textToCopy) return;

        navigator.clipboard.writeText(textToCopy).then(() => {
            showNotification();
        }).catch(err => {
            console.error("Не удалось скопировать: ", err);
        });
    });
});
