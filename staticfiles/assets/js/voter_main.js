"use srict";

const containerEl = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click',()=> 
containerEl.classList.add('active')
);

loginBtn.addEventListener('click',()=> 
containerEl.classList.remove('active')
);

document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.querySelector("#login");
    const registerBtn = document.querySelector("#register");
    const loginForm = document.querySelector(".login-form");
    const registerForm = document.querySelector(".register-form");
    const signupForm = document.querySelector('.signup-form');


    // Login button function
    loginBtn.addEventListener('click', () => {
        loginBtn.style.backgroundColor = "#21264D";
        registerBtn.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
        loginForm.style.left = "50%";
        registerForm.style.left = "-50%";
        loginForm.style.opacity = 1;
        registerForm.style.opacity = 0;
        document.querySelector(".col-1").style.borderRadius = "0 30% 20% 0";
    });

    // Register button function
    registerBtn.addEventListener('click', () => {
        loginBtn.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
        registerBtn.style.backgroundColor = "#21264D";
        loginForm.style.left = "150%";
        registerForm.style.left = "50%";
        loginForm.style.opacity = 0;
        registerForm.style.opacity = 1;
        document.querySelector(".col-1").style.borderRadius = "0 20% 30% 0";
    });

    // Signup form submission event listener
signupForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const aadharNumber = document.querySelector('input[name="aadhar_number"]').value;
    fetch(`/validate-aadhar/${aadharNumber}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If Aadhar number is valid, submit the form
                signupForm.submit();
            } else {
                // If Aadhar number is not valid, show error message
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

    // Login form submission logic
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const aadharNumber = document.querySelector('.login-form input[name="aadhar_number"]').value;
        const password = document.querySelector('.login-form input[name="password"]').value;

        fetch(`/validate-login/${aadharNumber}/${password}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.passwordType === 'primary') {
                        window.location.href = '/home.html';
                    } else if (data.passwordType === 'secondary') {
                        window.location.href = '/second.html';
                    }
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
