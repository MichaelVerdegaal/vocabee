function registerAccount(registerUrl, registerSuccessUrl) {
    /**
     * Sends an account registering request, and takes follow-action based on the response
     * @param {String} registerUrl - endpoint to send request to
     * @param {String} registerUrl - url to redirect to after successful register
     */
    let email = document.querySelector('#emailInput').value;
    let username = document.querySelector('#usernameInput').value;
    let password = document.querySelector('#passwordInput').value
    let passwordRepeat = document.querySelector('#passwordRepeatInput').value;

    postRequest(registerUrl, {email: email, username: username, password: password, password_repeat: passwordRepeat})
        .then(response => {
            return response.json();
        })
        .then(response => {
            let response_description = response.description;
            let continueRegisterFlow = response.body.continue_register;
            console.log(response_description);
            switch (continueRegisterFlow) {
                case 'false':
                    createAndShowToast(response_description)
                    break;
                case 'true':
                    window.location.replace(registerSuccessUrl);
                    break;
            }

        })
        .catch(error => {
            console.log(error);
            alert("Entry couldn't be added");
        });
}