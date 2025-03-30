function setupPlaceholderHandler(inputId, placeholderText) {
    const inputElement = document.getElementById(inputId);
    if (inputElement) {
        inputElement.addEventListener('focus', function () {
            if (this.value === '') {
                this.setAttribute('placeholder', '');
            }
        });

        inputElement.addEventListener('blur', function () {
            if (this.value === '') {
                this.setAttribute('placeholder', placeholderText);
            }
        });
    }
}

const fields = [
    { id: 'login', placeholder: 'Login' },
    { id: 'password', placeholder: 'Password' },
    { id: 'repeat-password', placeholder: 'Repeat Password' },
    { id: 'email', placeholder: 'Email' },
    { id: 'input-bio', placeholder: 'Write your bio here...' },
    { id: 'input-post-text', placeholder: 'Write your post here...' },
    { id: 'input-comment-text', placeholder: 'Write your comment here...' },
];

fields.forEach(field => setupPlaceholderHandler(field.id, field.placeholder));
