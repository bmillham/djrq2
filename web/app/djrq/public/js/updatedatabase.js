$(document).on('eldarion-ajax:success', function(evt, $el, data, textStatus, jqXHR) {
    var results = $(document).find('.results');
    results.html(data.html);

});

$(document).on('eldarion-ajax:begin', function(evt, $el, data, textStatus, jqXHR) {
    var results = $(document).find('.results');
    var dbupdate = $(document).find('.dbupdate');
    results.show();
    dbupdate.show();
    results.html('Update started');

});

