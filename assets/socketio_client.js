// assets/socketio_client.js

var socket = io();

socket.on('graph_update', function (data) {
    console.log("Received graph update from server");

    var store = document.querySelector('[data-dash-is-loading="false"][id="graph_update_store"]');
    if (store) {
        var event = new CustomEvent("graph_update_event", {detail: data});
        store.dispatchEvent(event);
    }
});