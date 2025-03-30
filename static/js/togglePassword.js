const passwordField = document.getElementById('password');
const togglePasswordButton = document.getElementById('togglePassword');
const showIcon = document.getElementById('showIcon');

togglePasswordButton.addEventListener('click', () => {
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
    showIcon.src = type === 'password' ? '../images/hide-password.png' : '../images/show-password.png';
});

const repeatPasswordField = document.getElementById('repeat-password');
const toggleRepeatPasswordButton = document.getElementById('toggleRepeatPassword');
const repeatShowIcon = document.getElementById('repeatShowIcon');

if (repeatPasswordField && toggleRepeatPasswordButton && repeatShowIcon) {
    toggleRepeatPasswordButton.addEventListener('click', () => {
        const type = repeatPasswordField.type === 'password' ? 'text' : 'password';
        repeatPasswordField.type = type;
        repeatShowIcon.src = type === 'password' ? '../images/hide-password.png' : '../images/show-password.png';
    });
}

