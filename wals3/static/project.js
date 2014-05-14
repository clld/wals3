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
