var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.hostname.split(':')[0] + '/sub?id=' + dj + '-admin';
//alert(url);
//var sub = new NchanSubscriber(url='http://websock.gelth.local/sub?id=' + window.location.hostname.split('.')[0], opt={subscriber:'websocket'});
var sub = new NchanSubscriber(url=url, opt={subscriber:'websocket'});

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message);
  if (m.progress == 100) {
      $('.dbupdate').text("Update Database");
  } else {
    $('.dbupdate').text('Update Progress: ' + m.progress);
  }
  $('.backupprogress').text(m.backupprogress);
});

sub.start();
