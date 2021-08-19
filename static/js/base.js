$( document ).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

function copyToClipboard(text_to_copy) {
    let $temp = $("<input>");
    $("body"). append($temp);
    $temp.val(text_to_copy).select();
    document. execCommand("copy");
    $temp. remove();
}