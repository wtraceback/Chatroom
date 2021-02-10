$(document).ready(function() {
    var socket = io('/')
    var message_count = 0

    var socketio_event = function() {
        socket.on('new message', function(msg) {
            if (!document.hasFocus()) {
                message_count++;
                document.title = '(' + message_count + ')' + 'Chatroom'
            }

            if (msg.user_id !== current_user_id) {
                message_notify(msg);
            }

            $('.messages').append(msg.data);
            flask_moment_render_all()
            scrollToBottom()
            activateSemantics()
        });

        socket.on('online users', function(msg) {
            $('#online-user').html(msg.data);
        });
    }

    var new_message_event = function() {
        // 按回车发送消息
        $('#message-textarea').on('keydown', function(e) {
            var message = $('#message-textarea').val().trim()
            if (e.key == "Enter" && !e.shiftKey && message) {
                e.preventDefault()
                socket.emit('new message', {data: message})
                $('#message-textarea').val('')
            }
        })

        // 当为移动窗口的时候，使用模态框
        $('#message-textarea').focus(function() {
            if (screen.width < 600) {
                $('#mobile-message-textarea-modal').modal('show')
                $('#message-textarea').blur()
                // $('#mobile-message-textarea').focus()
            }
        })

        // 点击模态框中的发送按钮
        $('#send-butn').on('click', function() {
            var message = $('#mobile-message-textarea').val().trim();
            if (message != '') {
                socket.emit('new message', {data: message})
                $('#mobile-message-textarea').val('')
            }
        })
    }

    var message_notify = function(msg) {
        if (Notification.permission !== 'granted') {
            Notification.requestPermission();
        } else {
            var notification = new Notification('Message from ' + msg.username, {
                icon: msg.gravatar,
                body: msg.body.replace(/(<([^>]+)>)/ig, "")
            });

            // 点击桌面消息时触发
            notification.onclick = function() {
                window.open(root_url);
                notification.close();
            };

            setTimeout(function() {
                notification.close();
            }, 5000);
        }
    }

    var __main = function() {
        socketio_event()
        new_message_event()

        // 桌面通知
        $(window).focus(function() {
            message_count = 0
            document.title = 'Chatroom'
        });
    }

    __main()
});
