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
    }, 'show');


    $("#vocab-table").DataTable({
        ajax: {
            url: endpoint,
            dataType: "json",
            dataSrc: "entries",
            contentType: "application/json; charset=utf-8",
        },
        columns: [
            {title: "ID", "data": "id"},
            {title: "Kanji", "data": "kanji"},
            {title: "Hiragana", "data": "hiragana"},
            {title: "English", "data": "english"},
            {
                title: "example_data",
                data: "examples",
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
 * @param {Array} columns - Details the construction of the columns
 */
function createExampleTable(examples, columns) {
    $("#example-table").DataTable({
        data: examples,
        columns: columns,
        paging: false,
        bSortClasses: false,
        deferRender: true,
        responsive: false,
        oLanguage: {
            "sEmptyTable": "No examples available for this entry..."
        },
    });
}