
document.getElementById('regForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmpassword").value;
    const passwordError = document.getElementById(
        "password-error"
    );

    passwordError.textContent = "";

    let isValid = true;

    if (password === "" || password.length < 6) {
        passwordError.textContent =
            "Please enter a password with at least 6 characters.";
        isValid = false;
    }

    if (password != confirmPassword) {
        passwordError.textContent =
            "the password dont match, please try again!!!";
        isValid = false;
    }


    if (isValid) {
        console.log("Form validated successfully, submitting form");
        event.target.submit();  }
        else {
            console.log("Form has validation errors, submission prevented");
        }
});
