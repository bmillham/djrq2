var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.hostname.split(':')[0] + '/sub?id=' + dj;
var sub = new NchanSubscriber(url=url, opt={subscriber:'websocket'});

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message)

  $('#listeners').html( m.listeners);
  $('#maxlisteners').html(m.maxlisteners);
  if ('requestbutton' in m) {
    $('#requestbutton').html(m.requestbutton);
    for(i=0;i<5;i++) {
        $('#requestbutton').fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
  }
  if ('request_row' in m) {
      $('#request-table tr:last').after(m.request_row);
      for(i=0;i<5;i++) {
        $('#request-table tr:last').fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
  }
  if ('request_id' in m) {
      $('#r_'+m.request_id).attr('disabled', 'disabled');
  }
});

sub.start();
