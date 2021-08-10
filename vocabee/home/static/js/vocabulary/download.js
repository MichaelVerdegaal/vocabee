function processDeckForm(requestUrl) {
    /**
     * Processes the flashcard form and downloads the deck file via a request
     * @param {String} requestUrl - Endpoint to send request to
     */
    let vocabLevel = document.querySelector('#levelSelectOne').value;
    let includeExamples = document.querySelector('#exampleCheckOne').checked;
    let downloadParams = {vocab_level: vocabLevel, include_examples: includeExamples}

    postRequest(requestUrl, downloadParams)
        .then(response => {
            return response.blob();
        })
        .then(response => {
            // Ref: https://stackoverflow.com/a/61313196/7174982
            const blob = new Blob([response], {type: 'application/octet-stream'});
            const downloadUrl = URL.createObjectURL(blob);
            const a = crel('a', {'href': downloadUrl, 'download': `vocabee${vocabLevel}.apkg`});
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => {
            console.log(error);
            alert("File can't be downloaded");
        });
}

function processFileForm(requestUrl) {
    /**
     * Processes the file form and downloads the specified file via a request
     * @param {String} requestUrl - Endpoint to send request to
     */
    let vocabLevel = document.querySelector('#levelSelectTwo').value;
    let fileType = document.querySelector('#fileFormatSelect').value;
    let includeExamples = document.querySelector('#exampleCheckTwo').checked;
    let downloadParams = {vocab_level: vocabLevel, file_type: fileType, include_examples: includeExamples}
    console.log(downloadParams)
}