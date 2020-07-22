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