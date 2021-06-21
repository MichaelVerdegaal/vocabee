const isOk = response => response.ok ? response.json() : Promise.reject(new Error('Failed the request'));

/**
 * Fill a bootstrap modal with a datatable
 *
 * @param {string} vocab_id - ID of vocabulary entry related to examples
 * @param {String} kanji - Example kanji
 * @param {String} kana - Example kana
 * @param {Array} examples - List of example sentences
 */
function fillExampleModal(vocab_id, kanji, kana, examples) {
    let modal_content = document.querySelector('#vocab-modal-body');
    modal_content.innerHTML = '';

    let exampleTableContainer = crel('div', {'id': 'example-table-container', 'class': 'container-fluid'});
    let exampleTable = crel('table', {'id': 'example-table', 'class': 'table table-striped table-hover'});

    exampleTableContainer.appendChild(exampleTable);
    modal_content.appendChild(exampleTableContainer);

    createExampleTable(examples, [
        {"title": "ID", "data": "id"},
        {"title": "Japanese", "data": "sentence_jp"},
        {"title": "English", "data": "sentence_en"}]);

    // Set modal title
    let modal_title = document.querySelector('#modalLargeLabel');
    modal_title.textContent = kanji !== '' ? `Showing examples for ${kanji}/${kana}` : `Showing examples for ${kana}`;
}

/**
 * On click action for the example button
 *
 * @param {array} row_data - Current row of the clicked button
 * @param {String} urlBase - Endpoint url to send request to
 */
function exampleOnClick(row_data, urlBase) {
    let vocab_id = row_data.id;
    let requestUrl = urlBase.slice(0, -1) + vocab_id;
    // Ref: https://stackoverflow.com/questions/7864723#7864740
    let kanji = row_data.kanji.split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];
    let kana = row_data.hiragana.split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            fillExampleModal(vocab_id, kanji, kana, data.entries);
        })
        .catch(error => {
            console.log(error);
            fillExampleModal(vocab_id, kanji, kana, []);
        });
}