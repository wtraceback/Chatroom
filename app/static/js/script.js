$(document).ready(function() {
    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });

    $('#toggle-sidebar').click(function() {
        $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
    })
});
