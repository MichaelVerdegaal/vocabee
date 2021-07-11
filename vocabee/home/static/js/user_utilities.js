function registerAccount(urlBase, email, username, password) {
    /**
     * todo
     * @param {String} urlBase - endpoint to send request to
     */

    postRequest(urlBase, {email: email, username: username, password: password})
        .then(isOk)
        .then(response => {
            console.log(response)
        })
        .catch(error => {
            console.log(error);
            alert("Entry couldn't be added");
        });
}