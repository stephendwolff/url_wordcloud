


$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    var $urlform = $("#urlform");

    $urlform.on("submit", function() {
        newURL($(this));
        return false;
    });
    $urlform.on("keypress", function(e) {
        if (e.keyCode === 13) {
            newURL($(this));
            return false;
        }
    });
    $("#url_for_wordcloud").select();
    updater.start();
});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


function newURL(form) {
    var url_for_wordcloud = $('#url_for_wordcloud').val();
    var urlform = {
        _xsrf: getCookie("_xsrf"),
        url_for_wordcloud: url_for_wordcloud
    };
    updater.socket.send(JSON.stringify(urlform));
    form.find("input[type=text]").val("").select();
}

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/analyse_url/";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showWordCloud(JSON.parse(event.data));
        };
        // show websocket has connected
        // TODO: monitor connection, and replace with 'connecting' if connection disrupted
        $('#websocket_connection').html('<i class="fas fa-check-square"></i> Connected');
    },

    showWordCloud: function(message) {
        alert (message);
        //        var existing = $("#wordcloud");
//        if (existing.length > 0) return;
//        var node = $(message.html);
//        node.hide();
//        $("#inbox").append(node);
//        node.slideDown();
    }
};
