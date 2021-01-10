$(document).ready(function() {
    var activateSemantics = function() {
        $('.message .close').on('click', function() {
            $(this).closest('.message').transition('fade');
        });

        $('#toggle-sidebar').click(function() {
            $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
        })
    }

    var scrollToBottom = function() {
        var $messages = $('.messages');
        if ($messages[0] != undefined) {
            $messages.scrollTop($messages[0].scrollHeight)
        }
    }

    var __main = function() {
        activateSemantics()
        scrollToBottom()
    }

    __main()
});
