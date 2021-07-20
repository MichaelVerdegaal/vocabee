function registerAccount(registerUrl, registerSuccessUrl) {
    /**
     * Sends an account registering request, and takes follow-action based on the response
     * @param {String} registerUrl - endpoint to send request to
     * @param {String} registerUrl - url to redirect to after successful register
     */
    let email = document.querySelector('#emailInput');
    let username = document.querySelector('#usernameInput');
    let password = document.querySelector('#passwordInput');
    let passwordRepeat = document.querySelector('#passwordRepeatInput');

    postRequest(registerUrl, {
        email: email.value,
        username: username.value,
        password: password.value,
        password_repeat: passwordRepeat.value
    })
        .then(response => {
            return response.json();
        })
        .then(response => {
            let continueRegisterFlow = response.body.continue_register;
            let fieldsReport = response.body.fields;

            switch (continueRegisterFlow) {
                case false:
                    if (fieldsReport.email.valid === 'true') {
                        email.className = "form-control is-valid";
                    } else {
                        email.className = "form-control is-invalid";
                        document.querySelector('#emailInvalidLabel').textContent = fieldsReport.email.error[0];
                    }
                    if (fieldsReport.username.valid === 'true') {
                        username.className = "form-control is-valid";
                    } else {
                        username.className = "form-control is-invalid";
                        document.querySelector('#usernameInvalidLabel').textContent = fieldsReport.username.error[0];
                    }
                    if (fieldsReport.password.valid === 'true') {
                        password.className = "form-control is-valid";
                    } else {
                        password.className = "form-control is-invalid";
                        document.querySelector('#passwordInvalidLabel').textContent = fieldsReport.password.error[0];
                    }
                    if (fieldsReport.password_repeat.valid === 'true') {
                        passwordRepeat.className = "form-control is-valid";
                    } else {
                        passwordRepeat.className = "form-control is-invalid";
                        document.querySelector('#passwordRepeatInvalidLabel').textContent = fieldsReport.password_repeat.error[0];
                    }
                    break;
                case true:
                    window.location.replace(registerSuccessUrl);
                    break;
            }

        })
        .catch(error => {
            console.log(error);
            alert("Entry couldn't be added");
        });
}