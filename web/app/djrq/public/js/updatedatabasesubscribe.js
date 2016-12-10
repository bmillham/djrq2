var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.hostname.split(':')[0] + '/sub?id=' + dj + '-admin';
var sub = new NchanSubscriber(url=url, opt={subscriber:'websocket'});

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message);
  if (m.progress == 100) {
      $('.dbupdate').text("Update Database");
  } else {
    $('.dbupdate').text('Update Progress: ' + m.progress);
  }
  //$('.backupprogress').text(m.backupprogress);
  if ("backupprogress" in m) {
      $('.backupprogress').text(m.backupprogress);
  }

  if ('stage' in m) {
      $('.stage h3').text(m.stage);
  }
  if ('currentfile' in m) {
    $('.currentartist').text(m.updateartist);
    $('.currentalbum').text(m.updatealbum);
    $('.currenttitle').text(m.updatetitle);
    $('.currentfile').text(m.currentfile);
    $('.currenttrack-table').show();
  }
  if (m.difference != null) {
    //var div = document.getElementById('difftable');
    //var content = document.createTextNode(m.difference + '<br>');
    //div.appendChild(content);
    $('.difftable').show();
    $('.difftable tr:first').after(m.difference);
    $('.updatedcount').text(m.updatedcount);
  }
  if (m.newtrack != null) {
      $('.newtrack-table').show();
      $('.newtrack-table tr:first').after(m.newtrack);
  }
  $('.update-progress-bar').css('width', m.progress+'%').attr('aria-valuenow', m.progress).text(m.progress+'%');
});

sub.start();
