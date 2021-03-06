$('#requestModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget)
    var title = button.data('title')
    var tid = button.data('tid')
    var modal = $(this)
    modal.find('.modal-title').text('Request: ' + title)
    modal.find('#tid').val(tid)
    modal.find('#comment').val(null)
    modal.find('#ricon').hide()
    modal.find('#requestform').show()
    modal.find('.results').text('')
    modal.find(".results").hide()
});

$('#mistagModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget)
    var title = button.data('title')
    var artist = button.data('artist')
    var album = button.data('album')
    var tid = button.data('tid')
    var modal = $(this)
    /* Set the modal to show the proper data, hide and show the proper elements */
    modal.find('.modal-title').text('Report Mistag: ' + title)
    modal.find('#tid').val(tid)
    modal.find('#title').val(title)
    modal.find('#artist').val(artist)
    modal.find('#album').val(album)
    modal.find('#comment').val(null)
    modal.find('#ricon').hide()
    modal.find('#mistagform').show()
    modal.find('.results').text('')
    modal.find(".results").hide()
});

$('#suggestionModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget)
    var modal = $(this)
    /* Set the modal to show the proper data, hide and show the proper elements */

    modal.find('#title').val('')
    modal.find('#artist').val('')
    modal.find('#album').val('')
    modal.find('#ricon').hide()
    modal.find('#comment').val(null)
    modal.find('#suggestionform').show()
    modal.find('.results').text('')
    modal.find(".results").hide()
});

$('#searchModal').on('show.bs.modal', function(event) {
    var modal = $(this);
    modal.find('#ricon').hide()
    modal.find('#searchform').show();
});

/* Event handlers for both request and mistag modals */
$(document).on('eldarion-ajax:begin', function(evt, $el) {
    var modal = $el.closest('.modal');
    var mid = modal.attr('id')
    $el.hide();
    modal.find('#ricon').show();
});

$(document).on('eldarion-ajax:success', function(evt, $el, data, textStatus, jqXHR) {
    var modal = $el.closest('.modal');
    var mid = modal.attr('id')
    if (mid == 'searchModal') {
        $(this).find('#main-content').html(data.html);
    } else {
        modal.find('#ricon').hide();
        modal.find('.results').show();
    }
});

$(document).on('eldarion-ajax:complete', function(evt, $el, data, textStatus, jqXHR) {
    var modal = $el.closest('.modal');
    var mid = modal.attr('id')
    var pre=''
    var newtext = ''
    $(this).find('.sitenickinput').attr('disabled', 'disabled')
    $(this).find('.sitenickinput').val(data.sitenick)
    $(this).find('[name="usericon"]').show()

    if (mid == 'requestModal') {
        pre='.r_';
        $(this).find('#requestbutton').text(data.newcount)
    } else if (mid == 'mistagModal') {
        pre='.m_';
    } else if (mid == 'searchModal') {
        modal.modal('hide');
        modal.find('#ricon').hide()
        return;
    }
    btn = $(this).find(pre + data.tid)
    btn.attr('disabled', 'disabled') // Grey out and disable the button
    setTimeout(function() {
        modal.modal('hide')
    }, 3000); // Show the thank you message for 3 seconds
});
