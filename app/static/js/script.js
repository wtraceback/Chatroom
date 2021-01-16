$(document).ready(function() {
    var activateSemantics = function() {
        var popupLoading = '<i class="notched circle loading icon teal"></i> Loading...';

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            }
        });

        $('.ui.dropdown').dropdown();
        $('.ui.checkbox').checkbox();

        $('.message .close').on('click', function() {
            $(this).closest('.message').transition('fade');
        });

        $('#toggle-sidebar').click(function() {
            $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
        })

        $('.popup-card').popup({
            inline: true,
            on: 'hover',
            html: popupLoading,
            hoverable: true,
            position: 'right center',
            offset: -40,
            delay: {
                show: 200,
                hide: 200
            },
            onShow: function() {
                var popup = this;
                popup.html(popupLoading);
                $.ajax({
                    url: $(popup).prev().data('href'),
                    method: 'get'
                }).done(function(result) {
                    popup.html(result);
                }).fail(function() {
                    popup.html('Failed to load profile.');
                });
            }
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
