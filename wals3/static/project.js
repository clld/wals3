WALS3 = {}

WALS3.formatLanguoid = function (obj) {
    var tag = 'u';

    if (!obj.text) {
        return 'search for a languoid'
    }

    if (obj.type == 'WalsLanguage') {
        tag = 'b';
    } else if (obj.type == 'Genus') {
        tag = 'i';
    }
    return '<' + tag + '>' + obj.text + '</' + tag + '>';
}

WALS3.reload = function (query) {
    var url, current = document.location;
    url = current.pathname;
    if (current.search) {
        query = $.extend({}, JSON.parse('{"' + decodeURI(current.search.replace('?', '').replace(/&/g, "\",\"").replace(/=/g,"\":\"")) + '"}'), query)
    }
    document.location.href = url + '?' + $.param(query);
}
