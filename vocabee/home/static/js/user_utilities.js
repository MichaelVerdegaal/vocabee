function registerAccount(urlBase) {
    /**
     * Sends an account registering request, and takes follow-action based on the response
     * @param {String} urlBase - endpoint to send request to
     */
    let email = document.querySelector('#emailInput').value;
    let username = document.querySelector('#usernameInput').value;
    let password = document.querySelector('#passwordInput').value
    let passwordRepeat = document.querySelector('#passwordRepeatInput').value;

    password = utf8_to_b64(password);
    passwordRepeat = utf8_to_b64(passwordRepeat);
    postRequest(urlBase, {email: email, username: username, password: password})
        .then(isOk)
        .then(response => {
            console.log(response.body)
        })
        .catch(error => {
            console.log(error);
            alert("Entry couldn't be added");
        });
}