function retrieveSearchData(searchUrlBase, searchResultUrlBase, searchQuery) {
    /**
     *  Makes a search request and sends the user to the search results page
     *
     *  @type {String} searchUrlBase - ajax endpoint to request a search
     *  @type {String} searchResultUrlBase - endpoint that renders search results page
     */
    let requestUrl = searchUrlBase.slice(0, -1) + searchQuery;

    fetch(requestUrl)
        .then(isOk)
        .then(data => {
            localStorage.matches = JSON.stringify(data);
            localStorage.searchQuery = searchQuery;
            location.href = searchResultUrlBase;
        })
        .catch(error => {
            localStorage.matches = JSON.stringify({
                'perfect_match_count': 0,
                'match_count': 0,
                'perfect_matches': [],
                'matches': []
            });
            localStorage.searchQuery = searchQuery;
            location.href = searchResultUrlBase;
        });
}


function doSearchIfInput(searchUrlBase, searchResultUrlBase, searchQuery) {
    /**
     *  Processes a search query if the input isn't empty
     *
     *  @type {String} searchUrlBase - ajax endpoint to request a search
     *  @type {String} searchResultUrlBase - endpoint that renders search results page
     *  @type {String} searchQuery - string of characters to look for
     */
    if (searchQuery !== '') {
        retrieveSearchData(searchUrlBase, searchResultUrlBase, searchQuery)

    }
}

function fillSearchPageFromResults(matchResults) {
    /**
     *  Fills the page with the search results
     * @type {Object} matchResults - search results
     */
    console.log(matchResults);
    let perfectMatchCount = matchResults.perfect_match_count;
    let perfectMatches = matchResults.perfect_matches;
    let fuzzyMatches = matchResults.matches;
    let fuzzyMatchCount = matchResults.match_count;
    let searchTime = matchResults.search_time;
    let searchQuery = localStorage.searchQuery;


    createVocabTable(perfectMatches, "#perfect-vocab-table", [
        {title: "ID", "data": "match_data.id"},
        {title: "Kanji", "data": "match_data.kanji"},
        {title: "Kana", "data": "match_data.kana"},
        {title: "English", "data": "match_data.english"},
        {title: "JLPT level", "data": "match_data.jlpt_level"},
    ]);

    if (fuzzyMatchCount > 0) {
        createVocabTable(fuzzyMatches, "#fuzzy-vocab-table", [
            {title: "ID", "data": "match_data.id"},
            {title: "Kanji", "data": "match_data.kanji"},
            {title: "Kana", "data": "match_data.kana"},
            {title: "English", "data": "match_data.english"},
            {title: "JLPT level", "data": "match_data.jlpt_level"},
            {title: "Similarity", "data": "fuzzy_ratio"}
        ])

        let fuzzyCollapseBtn = crel('btn', {
            'id': 'fuzzyMatchCollapseBtn',
            'class': 'btn btn-primary action-btn-gray',
            'data-bs-target': '#fuzzyMatchCollapse',
            'data-bs-toggle': 'collapse'
        }, 'Show ' + fuzzyMatchCount + ' low-similarity results')
        // Prevents responsiveness from breaking. Has something to do with the way the table is drawn in the collapse
        fuzzyCollapseBtn.addEventListener('click', function () {
            let table = $('#fuzzy-vocab-table').DataTable();
            table.columns.adjust().draw();
        })
        document.querySelector('#fuzzyMatchCollapse').before(fuzzyCollapseBtn)
    }

    let resultText = perfectMatchCount + " matches in " + searchTime + " seconds";
    if (!perfectMatchCount in window || searchTime in window) {
        resultText = "No results available for this search query"
    }
    document.querySelector('#resultCount').innerHTML = resultText;

    let searchResultTitleText = 'Search results';
    if (typeof searchQuery !== "undefined") {
        searchResultTitleText = 'Search results for "' + searchQuery + '"';
    }
    document.querySelector('#searchResultTitle').textContent = searchResultTitleText;
}