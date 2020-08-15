/**
 * Generate and fill a datatable with vocabulary data
 *
 * @param {string} level - JLPT level from 1-5
 *
 */
function createVocabTable(level) {
    let endpoint = "/vocab/source/" + level;

    let audio_button = document.createElement("button");
    audio_button.title = "Pronounce entry";
    audio_button.className = "btn-outline-primary audio-button";
    let audio_icon = document.createElement("i");
    audio_icon.className = "material-icons md-30";
    audio_icon.innerText = "volume_up";
    audio_button.appendChild(audio_icon);

    let example_button = document.createElement("button");
    example_button.type = "button";
    example_button.title = "Show examples";
    example_button.innerText = "show";
    example_button.className = "btn btn-outline-primary example-select";
    example_button.dataset.toggle = "modal";
    example_button.dataset.target = "#vocab-modal";

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
                title: "Audio",
                className: "audio-column",
                orderable: false,
                searchable: false,
                render: function () {
                    return audio_button.outerHTML
                }
            },
            {
                title: "Examples",
                class: "example-column",
                orderable: false,
                searchable: false,
                render: function () {
                    return example_button.outerHTML
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
            {width: '45%', targets: 3},
            {width: '5%', targets: 4},
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
 * @param {string} vocab_id - ID of vocabulary entry related to examples
 *
 */
function createExampleTable(vocab_id) {
    let endpoint = "/vocab/example/" + vocab_id;
    $("#example-table").DataTable({
        ajax: {
            url: endpoint,
            dataType: "json",
            dataSrc: "",
            contentType: "application/json; charset=utf-8",
        },
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
 *
 */
function fillExampleModal(vocab_id, kanji, hiragana) {
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

    createExampleTable(vocab_id);

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
    fillExampleModal(vocab_id, kanji, hiragana);
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