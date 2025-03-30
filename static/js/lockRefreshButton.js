document.addEventListener('scroll', function () {
    const refreshButton = document.getElementById('refresh');
    const footer = document.querySelector('footer');

    const footerTop = footer.getBoundingClientRect().top;
    const buttonHeight = refreshButton.offsetHeight;

    if (footerTop - window.innerHeight <= buttonHeight - 50) {
        const offset = buttonHeight - (footerTop - window.innerHeight) - 50;
        refreshButton.style.bottom = `${offset}px`;
    }
});
