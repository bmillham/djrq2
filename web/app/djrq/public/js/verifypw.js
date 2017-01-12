$('form').on('submit', function(){
    if($('#newpw').val() != $('#repeatnewpw').val()) {
        $('#np-label').text('Error: New Passwords Do Not Match');
        return false;
    }
    return true;
});
