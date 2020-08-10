/**
 * Generate and fill a datatable with vocabulary data
 *
 * @param {array} entries - Multidimensional array filled with vocabulary entries
 *
 */
function createVocabTable(level) {
    let endpoint = "/vocab/source/" + level;
    $("#vocab-table").DataTable({
        ajax: {
            url: endpoint,
            dataType: "json",
            dataSrc: "entries",
            contentType: "application/json; charset=utf-8",
        },
        pageLength: 8,
        lengthMenu: [[8, 25, 50], [8, 25, 50]],
        oLanguage: {
            "sLengthMenu": "Show _MENU_",
        },
        deferRender: true,
        bSortClasses: false,
        columns: [
            {title: "ID"},
            {title: "Kanji"},
            {title: "Hiragana"},
            {title: "English"},
            {
                title: "Pronounciation",
                orderable: false,
                searchable: false,
                render: function () {
                    return '<button title="Pronounce entry" class="btn-outline-primary pronounciation_button">' +
                        '<i class="material-icons md-30 ">volume_up</i>' +
                        '</button>'
                }
            },
            {
                title: "Examples",
                orderable: false,
                searchable: false,
                render: function () {
                    return '<button ' +
                        'type="button" ' +
                        'title="Show examples"' +
                        'class="btn btn-outline-primary example-select" ' +
                        'data-toggle="modal" ' +
                        'data-target="#vocab-modal">Show</button>'
                }
            }
        ],
        responsive: true
    });
}

/**
 * Generate and fill a datatable with example data
 *
 * @param {array} examples - Multidimensional array filled with example entries
 *
 */
function createExampleTable(endpoint) {
    $("#example-table").DataTable({
        ajax: {
            url: endpoint,
            dataType: "json",
            dataSrc: "",
            contentType: "application/json; charset=utf-8",
        },
        paging: false,
        bSortClasses: false,
        deferRender: true,
        columns: [
            {title: "ID"},
            {title: "Japanese"},
            {title: "English"}
        ],
        responsive: false
    });
}

/**
 * Fill a bootstrap modal with a datatable
 *
 * @param {array} examples - Multidimensional array filled with example entries
 * @param {String} kanji - Example kanji
 * @param {String} hiragana - Example hiragana
 *
 */
function fillExampleModal(endpoint, kanji, hiragana) {
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

    createExampleTable(endpoint);

    // Set modal title
    let modal_title = document.getElementById("modalLargeLabel");
    if (typeof kanji !== 'undefined') {
        modal_title.textContent = `Showing examples for ${kanji}/${hiragana}`;
    } else {
        modal_title.textContent = `Showing examples for ${hiragana}`;
    }
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
    let hiragana = row_data[2].split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];

    // Retrieving example data
    let endpoint = "/vocab/example/" + vocab_id;
    fillExampleModal(endpoint, kanji, hiragana);
}

/**
 * On click action for the pronounciation button
 *
 * @param {array} row_data - Current row of the clicked button
 * @param {Artyom} artyom - Artyom instance
 *
 */
function pronounciationOnClick(row_data, artyom) {
    // Ref: https://stackoverflow.com/questions/7864723#7864740
    let hiragana = row_data[2].split(/<a[^>]*>([\s\S]*?)<\/a>/)[1];
    artyom.say(hiragana);
}