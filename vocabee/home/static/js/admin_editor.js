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

function clearVocabFields() {
    /**
     * Clears the input vields from the vocabulary editor
     */
    document.querySelector('#vocabIDInput').value = '';
    document.querySelector('#kanjiOld').value = '';
    document.querySelector('#kanaOld').value = '';
    document.querySelector('#meaningOld').value = '';
    document.querySelector('#jlptOld').value = '';
    document.querySelector('#kanjiNew').value = '';
    document.querySelector('#kanaNew').value = '';
    document.querySelector('#meaningNew').value = '';
}

function clearExampleFields() {
    /**
     * Clears the input fields from the example editor
     */
    document.querySelector('#exampleIDInput').value = '';
    document.querySelector('#sentenceJPOld').value = '';
    document.querySelector('#sentenceJPNew').value = '';
    document.querySelector('#sentenceENOld').value = '';
    document.querySelector('#sentenceENNew').value = '';
}

function vocabEntryGet(urlBase) {
    /**
     * Retrieves a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let vocabID = document.querySelector('#vocabIDInput').value;
    let requestUrl = urlBase.slice(0, -1) + vocabID;
    clearVocabFields();

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            document.querySelector('#vocabIDInput').value = vocabID;
            document.querySelector('#kanjiOld').value = data.kanji;
            document.querySelector('#kanaOld').value = data.kana;
            document.querySelector('#meaningOld').value = data.english;
            document.querySelector('#jlptOld').value = data.jlpt_level;
            document.querySelector('#kanjiNew').value = data.kanji;
            document.querySelector('#kanaNew').value = data.kana;
            document.querySelector('#meaningNew').value = data.english;
            document.querySelector('#jlptNew').value = data.jlpt_level;

            localStorage.examples = JSON.stringify(data.examples);
        })
        .catch(error => {
            console.log(error);
            alert("Entry not found");
        });
}

function vocabEntryDelete(urlBase) {
    /**
     * Deletes a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to delete this entry?");
    if (c === true) {
        let vocabID = document.querySelector('#vocabIDInput').value;

        postRequest(urlBase, {id: vocabID})
            .then(isOk)
            .then(response => {
                alert("Entry " + vocabID + " deleted");
                clearVocabFields();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be deleted");
            });
    }
}

function vocabEntryUpdate(urlBase) {
    /**
     * Updates a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to update this entry?");
    if (c === true) {

        let vocabID = document.querySelector('#vocabIDInput').value;
        let kanji = document.querySelector('#kanjiNew').value;
        let kana = document.querySelector('#kanaNew').value;
        let meaning = document.querySelector('#meaningNew').value;
        let jlptLevel = document.querySelector('#jlptNew').value;

        postRequest(urlBase, {id: vocabID, kanji: kanji, kana: kana, meaning: meaning, jlpt_level: jlptLevel})
            .then(isOk)
            .then(response => {
                alert("Entry " + vocabID + " updated");
                clearVocabFields();
                document.querySelector('#vocabIDInput').value = vocabID;
                document.querySelector('#vocabEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be updated");
            });
    }
}

function vocabEntryAdd(urlBase) {
    /**
     * Adds a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to add this entry?");
    if (c === true) {
        let kanji = document.querySelector('#kanjiNew').value;
        let kana = document.querySelector('#kanaNew').value;
        let meaning = document.querySelector('#meaningNew').value;
        let jlptLevel = document.querySelector('#jlptNew').value;

        postRequest(urlBase, {kanji: kanji, kana: kana, meaning: meaning, jlpt_level: jlptLevel})
            .then(isOk)
            .then(response => {
                let vocabularyID = response.body.vocab_id;
                alert("Entry " + vocabularyID + " added");
                clearVocabFields();
                document.querySelector('#vocabIDInput').value = vocabularyID;
                document.querySelector('#vocabEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be added");
            });
    }
}

function exampleEntryGet(urlBase) {
    /**
     * Retrieves an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let exampleID = document.querySelector('#exampleIDInput').value;
    let requestUrl = urlBase.slice(0, -1) + exampleID;
    clearExampleFields();

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            document.querySelector('#exampleIDInput').value = exampleID;
            document.querySelector('#sentenceJPOld').value = data.sentence_jp;
            document.querySelector('#sentenceENOld').value = data.sentence_en;
            document.querySelector('#sentenceJPNew').value = data.sentence_jp;
            document.querySelector('#sentenceENNew').value = data.sentence_en;

        })
        .catch(error => {
            console.log(error);
            alert("Entry not found");
        });
}

function exampleEntryDelete(urlBase) {
    /**
     * Deletes an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to delete this entry?");
    if (c === true) {
        let exampleID = document.querySelector('#exampleIDInput').value;

        postRequest(urlBase, {id: exampleID})
            .then(isOk)
            .then(response => {
                alert("Entry " + exampleID + " deleted");
                clearExampleFields();
                document.querySelector('#vocabEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be deleted");
            });
    }
}

function exampleEntryUpdate(urlBase) {
    /**
     * Updates an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to update this entry?");
    if (c === true) {
        let exampleID = document.querySelector('#exampleIDInput').value;
        let sentenceJP = document.querySelector('#sentenceJPNew').value;
        let sentenceEN = document.querySelector('#sentenceENNew').value;

        postRequest(urlBase, {sentence_jp: sentenceJP, sentence_en: sentenceEN, id: exampleID})
            .then(isOk)
            .then(response => {
                alert("Entry " + exampleID + " updated");
                document.querySelector('#vocabEntryGetBtn').click();
                document.querySelector('#exampleEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be updated");
            });
    }
}

function exampleEntryAdd(urlBase) {
    /**
     * Adds an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to add this entry?");
    if (c === true) {
        let sentenceJP = document.querySelector('#sentenceJPNew').value;
        let sentenceEN = document.querySelector('#sentenceENNew').value;
        let vocabID = document.querySelector('#vocabIDInput').value;

        postRequest(urlBase, {sentence_jp: sentenceJP, sentence_en: sentenceEN, vocab_id: vocabID})
            .then(isOk)
            .then(response => {
                let exampleID = response.body.example_id;
                alert("Entry " + exampleID + " added");
                clearExampleFields();
                document.querySelector('#vocabEntryGetBtn').click();
                document.querySelector('#exampleIDInput').value = exampleID;
                document.querySelector('#exampleEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be added");
            });
    }
}

function fillExampleModal(kanji, kana, examples) {
    /**
     * Fills the example modal
     * @param {String} kanji - kanji item
     * @param {String} kana - kana item
     * @param {Array} exanokes - array of example sentences
     */
    let modal_content = document.querySelector("#example-modal-body");
    modal_content.innerHTML = '';

    let exampleTableContainer = crel('div', {'id': 'example-table-container', 'class': 'container-fluid'});
    let exampleTable = crel('table', {'id': 'example-table', 'class': 'table table-striped table-hover'});

    exampleTableContainer.appendChild(exampleTable);
    modal_content.appendChild(exampleTableContainer);

    let example_button = crel('button', {
        'type': 'button',
        'title': 'Select example',
        'id': 'selectExampleBtn',
        'class': 'btn btn-outline-primary exampleSelect',
    }, 'select');
    let example_columns = [
        {title: "ID"},
        {title: "English"},
        {title: "Japanese"},
        {title: "Select", data: null, "defaultContent": example_button.outerHTML}
    ];
    createExampleTable(examples, example_columns);

    // Set modal title
    let modal_title = document.querySelector("#modalLargeLabel");
    modal_title.textContent = kanji !== '' ? `Showing examples for ${kanji}/${kana}` : `Showing examples for ${kana}`;

    // Init onclick
    let exampleBtns = document.querySelectorAll('.exampleSelect');
    [...exampleBtns].map(btn => btn.addEventListener("click", function () {
        // Get data from all rows, including hidden ones. Ref: https://stackoverflow.com/a/38515622
        let current_row = $(this).parents('tr');
        if (current_row.hasClass('child')) {
            current_row = current_row.prev();
        }
        let row_data = $('#example-table').DataTable().row(current_row).data();

        document.querySelector('#exampleIDInput').value = row_data[0];
        $('#vocab-modal').modal('hide');
        document.querySelector('#exampleEntryGetBtn').click();
    }));
}

function showExampleOnClick() {
    /**
     * Shows the example datatable and fills it on button click
     */
    let kanji = document.querySelector('#kanjiNew').value;
    let kana = document.querySelector('#kanaNew').value;

    let examples = JSON.parse(localStorage.examples);
    examples.forEach(function (v) {
        delete v.vocab_id;
    });
    examples = examples.map(Object.values);

    fillExampleModal(kanji, kana, examples);
}

