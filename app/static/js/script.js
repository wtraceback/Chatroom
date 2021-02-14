var activateSemantics = function() {
    var popupLoading = '<i class="notched circle loading icon teal"></i> Loading...';

    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();

    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });

    $('#toggle-sidebar').click(function() {
        $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
    });

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

var page = 1;
var load_messages = function() {
    var position = $('.messages').scrollTop();
    if (position == 0) {
        page++;
        // 激活加载器
        $('.ui.loader').toggleClass('active');

        $.ajax({
            url: messages_url,
            type: 'GET',
            data: {page: page},
            success: function(data) {
                var before_height = $('.messages')[0].scrollHeight;
                $('.messages').prepend(data);
                var after_height = $('.messages')[0].scrollHeight;
                $('.messages').scrollTop(after_height - before_height);

                // 日期的渲染以及激活 semantic-ui 的 js 组件
                flask_moment_render_all();
                activateSemantics();

                // 关闭加载器
                $('.ui.loader').toggleClass('active');
            },
            error: function() {
                alert('No more messages.');
                // 关闭加载器
                $('.ui.loader').toggleClass('active');
            }
        })
    }
}

$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    var __main = function() {
        // 桌面通知
        document.addEventListener('DOMContentLoaded', function() {
            if (!Notification) {
                alert('Desktop notifications not available in your browser.');
                return;
            }

            if (Notification.permission !== 'granted') {
                Notification.requestPermission();
            }
        });

        activateSemantics();
        scrollToBottom();

        $('.messages').scroll(load_messages);
        $('#show-help-modal').click(function() {
            $('#help-modal').modal({blurring: true}).modal('show');
        });

        // delete message
        $('.delete-butn').on('click', function() {
            var confirm_result = confirm('Are you sure?')
            if (confirm_result) {
                var $this = $(this);
                $.ajax({
                    type: 'DELETE',
                    url: $this.data('href'),
                    success: function() {
                        $this.parent().parent().parent().remove();
                    },
                    error: function() {
                        alert('Oops, something was wrong.');
                    }
                })
            }
        });
    }

    __main()
});
