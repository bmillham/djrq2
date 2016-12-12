var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.hostname.split(':')[0] + '/sub?id=' + dj + '-admin';
var sub = new NchanSubscriber(url=url, opt={subscriber:'websocket'});

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message);
  if (m.progress == 100) {
      $('.dbupdate').text("Update Database");
  } else {
    $('.dbupdate').text('Update Progress: ' + m.progress + '%');
  }

  if ("backupprogress" in m) {
      $('.backupprogress').text(m.backupprogress);
  }

  if ('spinner' in m) {
      if (m.spinner) {
          $('#spinner').show();
      } else {
          $('#spinner').hide();
      }
  }

  if ('stage' in m) {
      $('#stage').text(m.stage);
  }
  if ('avetime' in m) {
      $('#avetime').text(m.avetime);
  }
  if ('checkedtracks' in m) {
      $('#checkedtracks').text(m.checkedtracks);
  }
  if ('totaltracks' in m) {
      $('#totaltracks').text(m.totaltracks);
  }
  if ('deletedtracks' in m) {
      $('#deletedtracks').text(m.deletedtracks);
  }
  if ('deletedrequests' in m) {
      $('#deletedrequests').text(m.deletedrequests);
  }
  if ('deletedplayed' in m) {
      $('#deletedplayed').text(m.deletedplayed);
  }
  if ('deletedmistags' in m) {
      $('#deletedmistags').text(m.deletedmistags);
  }
  if ('currentfile' in m) {
    $('.currentartist').text(m.updateartist);
    $('.currentalbum').text(m.updatealbum);
    $('.currenttitle').text(m.updatetitle);
    $('.currentfile').text(m.currentfile);
    $('.currenttrack-table').show();
  }
  if (m.difference != null) {
    $('.difftable').show();
    $('.difftable tr:first').after(m.difference);
    $('.updatedcount').text(m.updatedcount);
    $('#updatedtracks').text(m.updatedcount);
  }
  if (m.newtrack != null) {
      $('.newtrack-table').show();
      $('.newtrack-table tr:first').after(m.newtrack);
      $('.newcount').text(m.newcount);
      $('#addedtracks').text(m.newcount);
  }
  $('.update-progress-bar').css('width', m.progress+'%').attr('aria-valuenow', m.progress).text(m.progress+'%');
});

sub.start();
