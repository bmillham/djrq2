var sub = new NchanSubscriber(url='http://websock.gelth.local/sub?id=' + window.location.hostname.split('.')[0], opt={subscriber:'websocket'});

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message)

  $('#listeners').html( m.listeners);
  $('#maxlisteners').html(m.maxlisteners);
  $('#requestbutton').html(m.requestcount);

});

sub.start();
