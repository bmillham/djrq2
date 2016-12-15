var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.hostname.split(':')[0] + '/sub?id=' + dj;
var sub = new NchanSubscriber(url=url, opt={subscriber:'websocket'});

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message)

  $('#listeners').html( m.listeners);
  $('#maxlisteners').html(m.maxlisteners);
  $('#requestbutton').html(m.requestcount);

});

sub.start();
