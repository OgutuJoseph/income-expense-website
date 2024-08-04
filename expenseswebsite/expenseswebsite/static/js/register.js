const usernameField = document.querySelector('#usernameField')
const emailField = document.querySelector('#emailField')
const passwordField = document.querySelector('#passwordField')
const feedbackArea = document.querySelector('.invalid_feedback__username_class')
const emailFeedbackArea = document.querySelector('.invalid_email_feedback_class')
const usernameSuccessOutput = document.querySelector('.username_success_output')
const emailSuccessOutput = document.querySelector('.email_success_output')
const showPasswordToggle = document.querySelector('.show_password_toggle')

usernameField.addEventListener("keyup", (e) => {
    console.log('7777', 7777)
    const usernameVal = e.target.value;
    console.log('usernameVal', usernameVal)

    usernameSuccessOutput.style.display = 'block';
    usernameSuccessOutput.textContent = `Checking Username :: ${usernameVal}`;

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display = 'none';

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            usernameSuccessOutput.style.display = 'none';
            if (data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = 'block';
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
            }
        });
    }
    
});


emailField.addEventListener("keyup", (e) => {
    console.log('8888', 8888)
    const emailVal = e.target.value;
    
    emailSuccessOutput.style.display = 'block';
    emailSuccessOutput.textContent = `Checking Email :: ${emailVal}`;

    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display = 'none';

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            emailSuccessOutput.style.display = 'none';
            if (data.email_error){
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display = 'block';
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
            }
        });
    }
    
});

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "Show Password"){
        showPasswordToggle.textContent = "Hide"
        passwordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle.textContent = "Show Password"
        passwordField.setAttribute('type', 'password');
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput)