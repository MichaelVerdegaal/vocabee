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
                            crel('button', {'type':'button', 'class': 'btn-close', 'data-bs-dismiss': 'toast'})),
                        crel('div', {'class': 'toast-body'}, message)));
    toastContainer.append(toastEle);
    let bsAlert = new bootstrap.Toast(document.getElementById('liveToast'));
    bsAlert.show();
}