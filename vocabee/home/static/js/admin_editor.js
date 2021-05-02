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


function clearFields() {
    $('#vocab_id_input').val("");
    $('#kanjiOld').val("");
    $('#kanaOld').val("");
    $('#meaningOld').val("");
    $('#jlptOld').val("");
    $('#kanjiNew').val("");
    $('#kanaNew').val("");
    $('#meaningNew').val("");
}

function vocabEntryGet(urlBase) {
    let vocabID = $('#vocab_id_input').val();
    let requestUrl = urlBase.slice(0, -1) + vocabID;
    clearFields();

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
                clearFields();
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
                clearFields();
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
                clearFields();
                $('#vocab_id_input').val(vocabID);
            })
            .catch(error => {
                console.log(error);
                alert("Entry couldn't be added");
            })
    }
}