var sub = new NchanSubscriber(url='http://websock.gelth.local/sub?id=' + window.location.hostname.split('.')[0], opt={subscriber:'websocket'});

sub.on("message", function(message, message_metadata) {
  // message is a string
  // message_metadata may contain 'id' and 'content-type'
  var m = JSON.parse(message)
  $('#listeners').html( m.listeners);
  $('#maxlisteners').html(m.maxlisteners);
  $('#requestbutton').html(m.requestcount);
  //console.log("metadata: %o", message_metadata);
});

sub.start();
