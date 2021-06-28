function fillExampleModal(kanji, kana, examples) {
    /**
     * Fill a bootstrap modal with a datatable
     *
     * @param {String} kanji - Example kanji
     * @param {String} kana - Example kana
     * @param {Array} examples - List of example sentences
     */
    let modal_content = document.querySelector('#vocab-modal-body');
    modal_content.innerHTML = '';

    let exampleTableContainer = crel('div', {'id': 'example-table-container', 'class': 'container-fluid'});
    let exampleTable = crel('table', {'id': 'example-table', 'class': 'table table-striped table-hover browser-table'});

    exampleTableContainer.appendChild(exampleTable);
    modal_content.appendChild(exampleTableContainer);

    createExampleTable(examples, "#example-table", [
        {"title": "ID", "data": "id"},
        {"title": "Japanese", "data": "sentence_jp"},
        {"title": "English", "data": "sentence_en"}
    ]);

    // Set modal title
    let modal_title = document.querySelector('#modalLargeLabel');
    modal_title.textContent = kanji ? `Showing examples for ${kanji}/${kana}` : `Showing examples for ${kana}`;
}


function exampleOnClick(row_data, urlBase) {
    /**
     * On click action for the example button
     *
     * @param {array} row_data - Current row of the clicked button
     * @param {String} urlBase - Endpoint url to send request to
     */
    let vocabulary_id = row_data.id;
    let requestUrl = urlBase.slice(0, -1) + vocabulary_id;
    // Ref: https://stackoverflow.com/questions/7864723#7864740
    let kanji = row_data.kanji.split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];
    let kana = row_data.kana.split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            fillExampleModal(kanji, kana, data.entries);
        })
        .catch(error => {
            console.log(error);
            fillExampleModal(kanji, kana, []);
        });
}