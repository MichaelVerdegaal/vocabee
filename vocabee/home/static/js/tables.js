/**
 * Generate and fill a datatable with vocabulary data
 *
 * @param {string} vocabEndpoint - Endpoint to send AJAX request to
 * @param {string} level - JLPT level from 1-5
 *
 */
function createVocabTable(vocabEndpoint, level) {
    let endpoint = vocabEndpoint.slice(0, -1) + level;

    let example_button = crel('button', {
        'type': 'button',
        'title': 'Show examples',
        'id': 'selectExampleBtn',
        'class': 'btn btn-outline-primary example-select',
    }, 'show')


    $("#vocab-table").DataTable({
        ajax: {
            url: endpoint,
            dataType: "json",
            dataSrc: "entries",
            contentType: "application/json; charset=utf-8",
        },
        columns: [
            {title: "ID"},
            {title: "Kanji"},
            {title: "Hiragana"},
            {title: "English"},
            {
                title: "example_data",
                orderable: false,
                searchable: false,
                visible: false
            },
            {
                title: "Examples",
                class: "example-column",
                orderable: false,
                searchable: false,
                render: function () {
                    return example_button.outerHTML;
                }
            }
        ],
        deferRender: true,
        bSortClasses: false,
        responsive: true,
        autoWidth: false,
        columnDefs: [
            {width: '5%', targets: 0},
            {width: '10%', targets: 1},
            {width: '10%', targets: 2},
            {width: '50%', targets: 3},
            {width: '0%', targets: 3},
            {width: '5%', targets: 5},
        ],
        pageLength: 10,
        lengthMenu: [[10, 25, 50], [10, 25, 50]],
        pagingType: "full_numbers_no_ellipses",
        oLanguage: {
            "sLengthMenu": "Show _MENU_",
            "sEmptyTable": "No vocabulary available, something probably went wrong..."
        },
        language: {
            paginate: {
                previous: '<span class="material-icons">chevron_left</span>',
                next: '<span class="material-icons">chevron_right</span>',
                first: '<span class="material-icons">first_page</span>',
                last: '<span class="material-icons">last_page</span>'
            }
        }
    });
}


/**
 * Generate and fill a datatable with example data
 *
 * @param {Array} examples - List of example sentences
 */
function createExampleTable(examples) {
    $("#example-table").DataTable({
        data: examples,
        columns: [
            {title: "ID"},
            {title: "Japanese"},
            {title: "English"}
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

/**
 * Fill a bootstrap modal with a datatable
 *
 * @param {string} vocab_id - ID of vocabulary entry related to examples
 * @param {String} kanji - Example kanji
 * @param {String} hiragana - Example hiragana
 * @param {Array} examples - List of example sentences
 */
function fillExampleModal(vocab_id, kanji, hiragana, examples) {
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
    let examples = row_data[4]
    fillExampleModal(vocab_id, kanji, hiragana, examples);
}