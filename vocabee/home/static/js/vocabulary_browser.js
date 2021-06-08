/**
 * Fill a bootstrap modal with a datatable
 *
 * @param {string} vocab_id - ID of vocabulary entry related to examples
 * @param {String} kanji - Example kanji
 * @param {String} kana - Example kana
 * @param {Array} examples - List of example sentences
 */
function fillExampleModal(vocab_id, kanji, kana, examples) {
    let modal_content = document.getElementById("vocab-modal-body");
    modal_content.innerHTML = '';

    let exampleTableContainer = crel('div', {'id': 'example-table-container', 'class': 'container-fluid'})
    let exampleTable = crel('table', {'id': 'example-table', 'class': 'table table-striped table-hover'});

    exampleTableContainer.appendChild(exampleTable);
    modal_content.appendChild(exampleTableContainer);

    createExampleTable(examples, [{title: "ID"}, {title: "Japanese"}, {title: "English"}]);

    // Set modal title
    let modal_title = document.getElementById("modalLargeLabel");
    modal_title.textContent = kanji !== '' ? `Showing examples for ${kanji}/${kana}` : `Showing examples for ${kana}`;
}

/**
 * On click action for the example button
 *
 * @param {array} row_data - Current row of the clicked button
 *
 */
function exampleOnClick(row_data) {
    let vocab_id = row_data[0];
    // Ref: https://stackoverflow.com/questions/7864723#7864740
    let kanji = row_data[1].split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];
    let kana = row_data[2].split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];
    let examples = row_data[4]
    fillExampleModal(vocab_id, kanji, kana, examples);
}