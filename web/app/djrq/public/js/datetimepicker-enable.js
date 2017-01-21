function pad(number, length){
    var str = "" + number;
    while (str.length < length) {
        str = '0'+str;
    }
    return str;
}

var offset = new Date().getTimezoneOffset();
offset = ((offset<0? "+":"-")+
          pad(parseInt(Math.abs(offset/60)), 2)+
          pad(Math.abs(offset%60), 2));


$('.form_datetime').datetimepicker({
        //language:  'fr',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        forceParse: 0,
        showMeridian: 1,
        timezone: offset,
    });
