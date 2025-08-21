alert("Welcome to the Dream Journal App!");

document.addEventListener('DOMContentLoaded', (event) => {
    const heroSignUpButton = document.getElementById('signUp');
    const heroLogInButton = document.getElementById('logIn');
    const container1 = document.getElementById('container1');

    if (heroSignUpButton) {
        heroSignUpButton.addEventListener('click', () => {
            container1.scrollIntoView({ behavior: 'smooth' });
        });
    }

    if (heroLogInButton) {
        heroLogInButton.addEventListener('click', () => {
            container1.scrollIntoView({ behavior: 'smooth' });
        });
    }

});