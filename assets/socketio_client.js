
var socket = io();
socket.on('graph_update', function (data) {
    console.log("Received graph update from server", data);

    var store = document.getElementById('graph_update_store');
    if (store) {

        store.data = data;

        store.dispatchEvent(new CustomEvent('graph_update_event', { detail: data, bubbles: true }));
    }
});