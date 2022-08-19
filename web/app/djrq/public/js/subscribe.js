var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.host + '/sub?id=' + dj;
var sub = new NchanSubscriber(url=url, opt={subscriber:'websocket'});

function blink(el) {
    for(i=0;i<5;i++) {
        $(el).fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
}

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message)
  var newstat = null

  if ('new_request_status' in m) {
      var newstat = m.new_request_status;
      if (newstat == 'played' || newstat == 'delete' || newstat == 'ignored') {
          $('#rr_'+m.request_id).remove();
      }
  }

  if ('listeners' in m) {
    $('#listeners').html( m.listeners);
    blink($('#listeners'));
  }

  if ('maxlisteners' in m) {
    $('#maxlisteners').html(m.maxlisteners);
    blink($('#maxlisteners'));
  }

  if ('requestbutton' in m) {
    $('#requestbutton').html(m.requestbutton);
    blink($('#requestbutton'));
  }
  if ('request_row' in m) {
      if (newstat == null) {
        $('#request-table tr:last').after(m.request_row);
        blink($('#request-table tr:last'));
      } else {
        $('#rr_'+m.request_id).replaceWith(m.request_row);
        blink($('#rr'+m.request_id));
      }
  }
  if ('lastplay' in m) {
      $('#lastplay tr:first').after(m.lastplay);
      blink($('#lastplay td:first').parent());
  }
  if ('request_id' in m) {
      $('#r_'+m.request_id).attr('disabled', 'disabled');
  }

});

sub.start();
