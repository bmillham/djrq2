var dj = window.location.hostname.split('.')[0];
var url = 'http://' + window.location.host + '/sub?id=' + dj + '-admin';
var sub = new NchanSubscriber(url=url, opt={subscriber:'websocket'});

function blink(el) {
    for(i=0;i<5;i++) {
        $(el).fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
}

sub.on("message", function(message, message_metadata) {
  var m = JSON.parse(message);

  if ('requestbutton' in m) {
    $('#requestbutton').html(m.requestbutton);
    for(i=0;i<5;i++) {
        $('#requestbutton').fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
  }

  if ('listeners' in m) {
    $('#listeners').html( m.listeners);
  }

  if ('maxlisteners' in m) {
    $('#maxlisteners').html(m.maxlisteners);
  }

  if ('request_row' in m) {
      $('#request-table tr:last').after(m.request_row);
      for(i=0;i<5;i++) {
        $('#request-table tr:last').fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
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

  if ('r_spinner' in m) {
      if (m.r_spinner) {
          $('#r_spinner').show();
      } else {
          $('#r_spinner').hide();
      }
  }

  if ('updaterunning' in m) {
      if (m.updaterunning) {
          $('#updatedatabase-form').hide();
          $('#updaterunning').show();
          $('#progress-div').show();
          $('#noupdaterunning').hide();
      } else {
          $('#updaterunning').hide();
          $('#noupdaterunning').show()
      }
  }

  if ('historyfilename' in m) {
      $('#historyfilename').prop('href', m.historyfilename);
      $('#historyfilename').show();
  }


  if ('stage' in m) {
      $('#stage').text(m.stage);
  }
  if ('r_stage' in m) {
      $('#r_stage').text(m.r_stage);
  }
  if ('avetime' in m) {
      $('#avetime').text(m.avetime);
  }
  if ('Song_avetime' in m) {
      $('#Song_avetime').text(m.Song_avetime);
  }
  if ('RequestList_avetime' in m) {
      $('#RequestList_avetime').text(m.RequestList_avetime);
  }
  if ('Mistags_avetime' in m) {
      $('#Mistags_avetime').text(m.Mistags_avetime);
  }
  if ('Played_avetime' in m) {
      $('#Played_avetime').text(m.Played_avetime);
  }
  if ('checkedtracks' in m) {
      $('#checkedtracks').text(m.checkedtracks);
  }
  if ('Song_checkedtracks' in m) {
      $('#Song_checkedtracks').text(m.Song_checkedtracks);
  }
  if ('RequestList_checkedtracks' in m) {
      $('#RequestList_checkedtracks').text(m.RequestList_checkedtracks);
  }
  if ('Mistags_checkedtracks' in m) {
      $('#Mistags_checkedtracks').text(m.Mistags_checkedtracks);
  }
  if ('Played_checkedtracks' in m) {
      $('#Played_checkedtracks').text(m.Played_checkedtracks);
  }
  if ('Song_totaltracks' in m) {
      $('#Song_totaltracks').text(m.Song_totaltracks);
  }
  if ('Played_totaltracks' in m) {
      $('#Played_totaltracks').text(m.Played_totaltracks);
  }
  if ('RequestList_totaltracks' in m) {
      $('#RequestList_totaltracks').text(m.RequestList_totaltracks);
  }
  if ('Mistags_totaltracks' in m) {
      $('#Mistags_totaltracks').text(m.Mistags_totaltracks);
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
  if ('updatedcount' in m) {
      $('#updatedtracks').text(m.updatedcount);
  }
  if ('newcount' in m) {
      $('#addedtracks').text(m.newcount);
  }
  if ('difference' in m) {
    $('.difftable').show();
    $('.difftable tr:first').after(m.difference);
    $('.updatedcount').text(m.updatedcount);
    $('#updatedtracks').text(m.updatedcount);
  }
  if ('newtrack' in m) {
      $('.newtrack-table').show();
      $('.newtrack-table tr:first').after(m.newtrack);
      $('.newcount').text(m.newcount);
      $('#addedtracks').text(m.newcount);
  }
  if ('active' in m) {
      if (m.active) {
          $('#progress').addClass('active');
      } else {
          $('#progress').removeClass('active');
      }
  }
  if ('r_active' in m) {
      if (m.r_active) {
          $('#r_progress').addClass('active');
      } else {
          $('#r_progress').removeClass('active');
      }
  }

  if ('progress' in m) {
    $('.update-progress-bar').css('width', m.progress+'%').attr('aria-valuenow', m.progress).text(m.progress+'%');
    if (m.progress < 100) {
    //  $('.dbupdate').text("Update Database");
    //} else {
      $('#updateprogress').text('Update Progress: ' + m.progress + '%');
    }

  }

  if ('r_progress' in m) {
    $('#r_progress').css('width', m.r_progress+'%').attr('aria-valuenow', m.r_progress).text(m.r_progress+'%');
    if (m.r_progress < 100) {
    //  $('.dbupdate').text("Update Database");
    //    $('#updateprogress').text("Update Progress");
    //} else {
    //  $('.dbupdate').text('Restore Progress: ' + m.r_progress + '%');
        $('#updateprogress').text('Restore Progress: ' + m.r_progress + '%');
    }

  }
});

sub.start();
