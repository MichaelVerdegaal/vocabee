const isOk = response => response.ok ? response.json() : Promise.reject(new Error('Failed the request'))

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
    })
}


function clearVocabFields() {
    /**
     * Clears the input vields from the vocabulary editor
     */
    $('#vocab_id_input').val("");
    $('#kanjiOld').val("");
    $('#kanaOld').val("");
    $('#meaningOld').val("");
    $('#jlptOld').val("");
    $('#kanjiNew').val("");
    $('#kanaNew').val("");
    $('#meaningNew').val("");
}

function clearExampleFields() {
    /**
     * Clears the input fields from the example editor
     */
    $('#example_id_input').val("")
    $('#sentenceJPOld').val("");
    $('#sentenceJPNew').val("");
    $('#sentenceENOld').val("");
    $('#sentenceENNew').val("");
}

function vocabEntryGet(urlBase) {
    /**
     * Retrieves a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let vocabID = $('#vocab_id_input').val();
    let requestUrl = urlBase.slice(0, -1) + vocabID;
    clearVocabFields();

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            $('#vocab_id_input').val(vocabID);
            $('#kanjiOld').val(data.kanji);
            $('#kanaOld').val(data.hiragana);
            $('#meaningOld').val(data.english);
            $('#jlptOld').val(data.jlpt_level);
            $('#kanjiNew').val(data.kanji);
            $('#kanaNew').val(data.hiragana);
            $('#meaningNew').val(data.english);
            $('#jlptNew').val(data.jlpt_level);
            let examples = data.examples;
            localStorage['examples'] = JSON.stringify(examples);
        })
        .catch(error => {
            console.log(error);
            alert("Entry not found");
        })
}

function vocabEntryDelete(urlBase) {
    /**
     * Deletes a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to delete this entry?")
    if (c === true) {
        let vocabID = $('#vocab_id_input').val();

        postRequest(urlBase, {id: vocabID})
            .then(isOk)
            .then(response => {
                alert("Entry " + vocabID + " deleted");
                clearVocabFields();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be deleted");
            })
    }
}

function vocabEntryUpdate(urlBase) {
    /**
     * Updates a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to update this entry?")
    if (c === true) {
        let vocabID = $('#vocab_id_input').val();
        let kanji = $('#kanjiNew').val();
        let kana = $('#kanaNew').val();
        let meaning = $('#meaningNew').val();
        let jlpt_level = $('#jlptNew').val();

        postRequest(urlBase, {id: vocabID, kanji: kanji, kana: kana, meaning: meaning, jlpt_level: jlpt_level})
            .then(isOk)
            .then(response => {
                alert("Entry " + vocabID + " updated");
                clearVocabFields();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be updated");
            })
    }
}

function vocabEntryAdd(urlBase) {
    /**
     * Adds a vocabulary entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to add this entry?")
    if (c === true) {
        let kanji = $('#kanjiNew').val();
        let kana = $('#kanaNew').val();
        let meaning = $('#meaningNew').val();
        let jlpt_level = $('#jlptNew').val();

        postRequest(urlBase, {kanji: kanji, kana: kana, meaning: meaning, jlpt_level: jlpt_level})
            .then(isOk)
            .then(response => {
                let vocabID = response.body.vocab_id;
                alert("Entry " + vocabID + " added");
                clearVocabFields();
                $('#vocab_id_input').val(vocabID);
                $('#vocabEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be added");
            })
    }
}

function exampleEntryGet(urlBase) {
    /**
     * Retrieves an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let exampleID = $('#example_id_input').val();
    let requestUrl = urlBase.slice(0, -1) + exampleID;
    clearExampleFields();

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            $('#example_id_input').val(exampleID);
            $('#sentenceJPOld').val(data.sentence_jp);
            $('#sentenceENOld').val(data.sentence_en);
            $('#sentenceJPNew').val(data.sentence_jp);
            $('#sentenceENNew').val(data.sentence_en);
        })
        .catch(error => {
            console.log(error);
            alert("Entry not found");
        })
}

function exampleEntryDelete(urlBase) {
    /**
     * Deletes an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to delete this entry?")
    if (c === true) {
        let example_id = $('#example_id_input').val();

        postRequest(urlBase, {id: example_id})
            .then(isOk)
            .then(response => {
                alert("Entry " + example_id + " deleted");
                clearExampleFields();
                $('#vocabEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be deleted");
            })
    }
}

function exampleEntryUpdate(urlBase) {
    /**
     * Updates an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to update this entry?")
    if (c === true) {
        let example_id = $('#example_id_input').val();
        let sentence_jp = $('#sentenceJPNew').val();
        let sentence_en = $('#sentenceENNew').val();

        postRequest(urlBase, {sentence_jp: sentence_jp, sentence_en: sentence_en, id: example_id})
            .then(isOk)
            .then(response => {
                alert("Entry " + example_id + " updated");
                $('#vocabEntryGetBtn').click();
                $('#exampleEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be updated");
            })
    }
}

function exampleEntryAdd(urlBase) {
    /**
     * Adds an example entry
     * @param {String} urlBase - endpoint to send request to
     */
    let c = confirm("Are you sure you want to add this entry?")
    if (c === true) {
        let sentence_jp = $('#sentenceJPNew').val();
        let sentence_en = $('#sentenceENNew').val();
        let vocab_id = $('#vocab_id_input').val();

        postRequest(urlBase, {sentence_jp: sentence_jp, sentence_en: sentence_en, vocab_id: vocab_id})
            .then(isOk)
            .then(response => {
                let exampleID = response.body.example_id;
                alert("Entry " + exampleID + " added");
                clearExampleFields();
                $('#vocabEntryGetBtn').click();
                $('#example_id_input').val(exampleID);
                $('#exampleEntryGetBtn').click();
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be added");
            })
    }
}

function createExampleTable(examples) {
    /**
     * Creates an example datatable
     * @param {Array} examples - array of example sentences
     */
    let example_button = crel('button', {
        'type': 'button',
        'title': 'Select example',
        'id': 'selectExampleBtn',
        'class': 'btn btn-outline-primary example-select',
    }, 'select')


    $("#example-table").DataTable({
        data: examples,
        columns: [
            {title: "ID"},
            {title: "English"},
            {title: "Japanese"},
            {
                data: null,
                "defaultContent": example_button.outerHTML
            }

        ],
        paging: false,
        bSortClasses: false,
        deferRender: true,
        responsive: false,
        oLanguage: {
            "sEmptyTable": "No examples available for this entry..."
        },
    });
}

function fillExampleModal(vocab_id, kanji, kana, examples) {
    /**
     * Fills the example modal
     * @param {String} vocab_id - vocabulary id
     * @param {String} kanji - kanji item
     * @param {String} kana - kana item
     * @param {Array} exanokes - array of example sentences
     */
    let modal_content = document.getElementById("vocab-modal-body");
    modal_content.innerHTML = '';

    let exampleTableContainer = crel('div', {'id': 'example-table-container', 'class': 'container-fluid'})
    let exampleTable = crel('table', {'id': 'example-table', 'class': 'table table-striped table-hover'});

    exampleTableContainer.appendChild(exampleTable);
    modal_content.appendChild(exampleTableContainer);

    createExampleTable(examples);

    // Set modal title
    let modal_title = document.getElementById("modalLargeLabel");
    modal_title.textContent = kanji !== '' ? `Showing examples for ${kanji}/${kana}` : `Showing examples for ${kana}`;

    // Init onclick
    $('.example-select').click(function () {
        // Get data from all rows, including hidden ones. Ref: https://stackoverflow.com/a/38515622
        let current_row = $(this).parents('tr');
        if (current_row.hasClass('child')) {
            current_row = current_row.prev();
        }
        let row_data = $('#example-table').DataTable().row(current_row).data();

        let example_id = row_data[0];
        $('#example_id_input').val(example_id);
        $('#vocab-modal').modal('hide');
        $('#exampleEntryGetBtn').click();
    });
}

function showExampleOnClick() {
    /**
     * Shows the example datatable and fills it on button click
     */
    let vocabID = $('#vocab_id_input').val();
    let kanji = $('#kanjiOld').val();
    let kana = $('#kanaOld').val();

    let examples = JSON.parse(localStorage['examples']);
    examples.forEach(function (v) {
        delete v.vocab_id
    });
    examples = examples.map(Object.values);

    fillExampleModal(vocabID, kanji, kana, examples);
}

