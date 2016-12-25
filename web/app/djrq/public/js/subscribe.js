var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.hostname.split(':')[0] + '/sub?id=' + dj;
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

  $('#listeners').html( m.listeners);
  $('#maxlisteners').html(m.maxlisteners);

  if ('requestbutton' in m) {
    $('#requestbutton').html(m.requestbutton);
    for(i=0;i<5;i++) {
        $('#requestbutton').fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
  }
  if ('request_row' in m) {
      if (newstat == null) {
        $('#request-table tr:last').after(m.request_row);
      } else {
        $('#rr_'+m.request_id).replaceWith(m.request_row);
      }
      for(i=0;i<5;i++) {
        $('#rr_'+m.request_id).fadeTo('slow', 0.1).fadeTo('slow', 1.0);
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
