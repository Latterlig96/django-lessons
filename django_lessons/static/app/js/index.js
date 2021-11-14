$(document).ready(function() {
    $(window).click(function() {
        $('#profile-menu').removeClass('show-profile-menu');
    });
    $('.profile-button').click(function(event) {
        event.stopPropagation();
    });
});