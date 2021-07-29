const PAGINATE = {
    previous: '<i class="bi bi-chevron-left"></i>',
    next: '<i class="bi bi-chevron-right"></i>',
    first: '<i class="bi bi-chevron-bar-left"></i>',
    last: '<i class="bi bi-chevron-bar-right"></i>'
}

// TODO: make a clear decision between having the objects in strings or not, for consistency sake
function createVocabBrowserTable(vocabEndpoint, table_id, level) {
    /**
     * Generate and fill a datatable with vocabulary data sourced from an endpoint. Includes example button
     *
     * @param {string} vocabEndpoint - Endpoint to send AJAX request to
     * @param {String} table_id - Selector to init table on
     * @param {string} level - JLPT level from 1-5
     *
     */
    let endpoint = vocabEndpoint.slice(0, -1) + level;

    let example_button = crel('button', {
        'type': 'button',
        'title': 'Show examples',
        'id': 'selectExampleBtn',
        'class': 'btn btn-outline-primary example-select',
    }, 'show');


    $(table_id).DataTable({
        ajax: {
            url: endpoint,
            dataType: "json",
            dataSrc: "entries",
            contentType: "application/json; charset=utf-8",
        },

        columns: [
            {title: "ID", "data": "id"},
            {title: "Kanji", "data": "kanji"},
            {title: "Kana", "data": "kana"},
            {title: "English", "data": "english"},
            {
                data: "id",
                title: "Examples",
                class: "example-column",
                orderable: false,
                searchable: false,
                render: function () {
                    return example_button.outerHTML;
                }
            }
        ],
        columnDefs: [
            {width: '5%', targets: 0},
            {width: '10%', targets: 1},
            {width: '10%', targets: 2},
            {width: '50%', targets: 3},
            {width: '5%', targets: 4},
        ],

        deferRender: true,
        bSortClasses: false,
        responsive: true,
        autoWidth: false,

        pageLength: 10,
        lengthMenu: [[10, 25, 50], [10, 25, 50]],
        pagingType: "full_numbers_no_ellipses",
        oLanguage: {
            "sLengthMenu": "Show _MENU_",
            "sEmptyTable": "No vocabulary available, something probably went wrong..."
        },
        language: {
            paginate: PAGINATE
        }
    });
}

function createVocabTable(vocabulary, table_id, columns) {
    /**
     * Generate and fill a datatable with vocabulary data
     *
     * @param {Array} vocabulary - Vocabulary data
     * @param {String} table_id - Selector to init table on
     *
     */
    $(table_id).DataTable({
        data: vocabulary,
        dataType: "json",
        dataSrc: "entries",
        deferRender: true,
        bSortClasses: false,
        responsive: true,
        autoWidth: false,
        columns: columns,
        pageLength: 10,
        lengthMenu: [[10, 25, 50], [10, 25, 50]],
        pagingType: "full_numbers_no_ellipses",
        oLanguage: {
            "sLengthMenu": "Show _MENU_",
            "sEmptyTable": "No matches..."
        },
        language: {
            paginate: PAGINATE
        }
    });
}

function createExampleTable(examples, table_id, columns) {
    /**
     * Generate and fill a datatable with example data
     *
     * @param {Array} examples - List of example sentences
     * @param {String} table_id - Selector to init table on
     * @param {Array} columns - Details the construction of the columns
     */
    $(table_id).DataTable({
        data: examples,
        columns: columns,
        paging: false,
        bSortClasses: false,
        deferRender: true,
        responsive: true,
        oLanguage: {
            "sEmptyTable": "No examples available for this entry..."
        },
    });
}