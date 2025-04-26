var socket = io();

socket.on('graph_update', function (data) {
    console.log("Received graph update from server");

    var store = document.getElementById('graph_update_store');
    if (store) {
        store.value = JSON.stringify(data);
        store.dispatchEvent(new Event('input', { bubbles: true }));
    }
});