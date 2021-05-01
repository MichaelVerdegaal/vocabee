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

    $.ajax({
        url: requestUrl,
        type: "GET",
        success: function (result) {
            if (result === "") {
                alert("Entry not found");
            } else {
                $('#vocab_id_input').val(vocabID);
                $('#kanjiOld').val(result.kanji);
                $('#kanaOld').val(result.hiragana);
                $('#meaningOld').val(result.english);
                $('#jlptOld').val(result.jlpt_level);
                $('#kanjiNew').val(result.kanji);
                $('#kanaNew').val(result.hiragana);
                $('#meaningNew').val(result.english);
                $('#jlptNew').val(result.jlpt_level);
            }
        }
    });
}

function vocabEntryDelete(urlBase) {
    let c = confirm("Are you sure you want to delete this entry?")
    if (c === true) {
        let vocabID = $('#vocab_id_input').val();

        $.ajax({
            url: urlBase,
            type: "POST",
            data: {id: vocabID},
        });

        clearFields();
        alert("Entry " + vocabID + " deleted");
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
        console.log(jlpt_level);

        $.ajax({
            url: urlBase,
            type: "POST",
            data: {id: vocabID, kanji: kanji, kana: kana, meaning: meaning, jlpt_level: jlpt_level},
        });

        alert("Entry " + vocabID + " updated");
    }
}

function vocabEntryAdd(urlBase) {
    let c = confirm("Are you sure you want to add this entry?")
    if (c === true) {
        let kanji = $('#kanjiNew').val();
        let kana = $('#kanaNew').val();
        let meaning = $('#meaningNew').val();
        let jlpt_level = $('#jlptNew').val();

        $.ajax({
            url: urlBase,
            type: "POST",
            data: {kanji: kanji, kana: kana, meaning: meaning, jlpt_level: jlpt_level},
        });

        alert("Entry " + 0 + " updated");
    }
}