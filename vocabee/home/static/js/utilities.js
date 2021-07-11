const isOk = response => response.ok ? response.json() : Promise.reject(new Error('Failed the request'));

function postRequest(url, data) {
    /**
     * Helper function to send a post request.
     */
    return fetch(url, {
        credentials: 'same-origin',
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'},
    });
}

function createAndShowToast(message) {
    /**
     * Creates a toast, appends it to a toastContainer and shows it
     * @type {String} message - toast message
     */
    let toastContainer = document.getElementById('toastContainer')
    toastContainer.innerHTML = '';
    let toastEle = crel('div', {'class': 'position-fixed bottom-0 end-0 p-3', 'style': 'z-index: 11'},
        crel('div', {'id': 'liveToast', 'class': 'toast hide', 'role': 'alert'},
            crel('div', {'class': 'toast-header'},
                crel('strong', {'class': 'me-auto'}, 'Alert'),
                crel('small', 'just now'),
                crel('button', {'type': 'button', 'class': 'btn-close', 'data-bs-dismiss': 'toast'})),
            crel('div', {'class': 'toast-body'}, message)));
    toastContainer.append(toastEle);
    let bsAlert = new bootstrap.Toast(document.getElementById('liveToast'));
    bsAlert.show();
}

function utf8_to_b64(str) {
    /**
     * Encodes a string to base64, following https://developer.mozilla.org/en-US/docs/Glossary/Base64
     * @type {String} str - string to encode
     */
    return window.btoa(unescape(encodeURIComponent(str)));
}