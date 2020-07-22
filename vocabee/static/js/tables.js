function createDataTable(target, dataset, pageLength, lengthMenu, columns) {
    $(target).DataTable({
        data: dataset,
        pageLength: pageLength,
        lengthMenu: lengthMenu,
        columns: columns,
        responsive: true
    });
}

function createVocabTable() {
    createDataTable(
        '#vocab-table',
        entries,
        8,
        [[8, 25, 50], [8, 25, 50]],
        [
            {title: "ID"},
            {title: "Kanji"},
            {title: "Hiragana"},
            {title: "English"},
            {
                title: "Examples",
                orderable: false,
                searchable: false,
                render: function () {
                    return '<button ' +
                        'type="button" ' +
                        'class="btn btn-outline-primary" ' +
                        'id="example-select" ' +
                        'data-toggle="modal" ' +
                        'data-target="#vocab-modal">Show</button>\n'
                }
            }
        ]);
}

function fillExampleModal(data, kanji, hiragana) {
    // Fill modal with examples
    let modal_content = document.getElementById("vocab-modal-body");
    modal_content.innerHTML = '';
    let example_count = data.length;
    if (example_count > 0) {
        for (let e of data) {
            let paragraph = document.createElement("p");
            paragraph.innerHTML = `${e[1]}<br>${e[2]}<br>`;
            modal_content.appendChild(paragraph);
        }
    } else {
        let paragraph = document.createElement("p");
        paragraph.innerHTML = `Sorry, no examples for this entry...`;
        modal_content.appendChild(paragraph);
    }

    // Set modal title
    let modal_title = document.getElementById("modalLargeLabel");
    let example_text = "examples";
    if (example_count === 1) {
        example_text = "example";
    }
    if (typeof kanji !== 'undefined') {
        modal_title.textContent = `Showing ${example_count} ${example_text} for ${kanji}/${hiragana}`;
    } else {
        modal_title.textContent = `Showing ${example_count} ${example_text} for ${hiragana}`;
    }
}