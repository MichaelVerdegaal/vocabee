const isOk = response => response.ok ? response.json() : Promise.reject(new Error('Failed the request'))

function postRequest(url, data) {
    return fetch(url, {
        credentials: 'same-origin',
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'},
    })
}


function clearVocabFields() {
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
    $('#example_id_input').val("")
    $('#sentenceJPOld').val("");
    $('#sentenceJPNew').val("");
    $('#sentenceENOld').val("");
    $('#sentenceENNew').val("");
}


function vocabEntryGet(urlBase) {
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
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be added");
            })
    }
}

function exampleEntryGet(urlBase) {
    let exampleID = $('#example_id_input').val();
    let requestUrl = urlBase.slice(0, -1) + exampleID;
    clearExampleFields();

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            $('#example_id_input').val(exampleID);
            $('#sentenceJPOld').val(data.sentence_jp);
            $('#sentenceENOld').val(data.sentence_en);
        })
        .catch(error => {
            console.log(error);
            alert("Entry not found");
        })
}


function createExampleTable(examples) {
    let example_button = document.createElement("button");
    example_button.type = "button";
    example_button.title = "Select example";
    example_button.innerText = "select";
    example_button.className = "btn btn-outline-primary example-select";
    example_button.id = "selectExampleBtn";


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


function fillExampleModal(vocab_id, kanji, hiragana, examples) {
    let modal_content = document.getElementById("vocab-modal-body");
    modal_content.innerHTML = '';

    let exampleTableContainer = document.createElement("div");
    exampleTableContainer.className = "container-fluid";
    exampleTableContainer.id = "example-table-container";

    let exampleTable = document.createElement("table");
    exampleTable.className = "table table-striped table-hover";
    exampleTable.id = "example-table";

    exampleTableContainer.appendChild(exampleTable);
    exampleTableContainer.appendChild(document.createElement("th"));
    modal_content.appendChild(exampleTableContainer);

    createExampleTable(examples);

    // Set modal title
    let modal_title = document.getElementById("modalLargeLabel");
    if (typeof kanji !== 'undefined') {
        modal_title.textContent = `Showing examples for ${kanji}/${hiragana}`;
    } else {
        modal_title.textContent = `Showing examples for ${hiragana}`;
    }

    // Init onclick
    $('.example-select').click(function () {
        console.log('No')
    });
}

function showExampleOnClick() {
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

