
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const signUpBtn = document.getElementById('signUpBtn');
const signInBtn = document.getElementById('signInBtn');
const mobileBackBtn = document.getElementById('mobileBackBtn');
const container = document.getElementById('container');

// Desktop overlay buttons
signUpButton.addEventListener('click', () => {
    container.classList.add("signup-mode");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("signup-mode");
});

// Text link buttons (work on both desktop and mobile)
signUpBtn.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
        container.classList.add("mobile-signup");
    } else {
        container.classList.add("signup-mode");
    }
});

signInBtn.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
        container.classList.remove("mobile-signup");
    } else {
        container.classList.remove("signup-mode");
    }
});

// Mobile back button
mobileBackBtn.addEventListener('click', () => {
    container.classList.remove("mobile-signup");
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        container.classList.remove("mobile-signup");
    }
});
