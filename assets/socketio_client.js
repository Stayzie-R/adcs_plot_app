var socket = io();

socket.on('graph_update', function (data) {
    console.log("Received graph update from server", data);  // Logování přijatých dat

    var store = document.getElementById('graph_update_store');
    if (store) {
        console.log("Updating store with new data", data);  // Logování, že data budou předána do Store
        store.value = JSON.stringify(data);
        store.dispatchEvent(new Event('input', { bubbles: true }));
    } else {
        console.error("Store element not found!");  // Pokud store neexistuje
    }
});

// Pro sledování připojení a detekci případných problémů
socket.on('connect', function() {
    console.log('Socket.io client connected');
});

socket.on('disconnect', function() {
    console.error('Socket.io client disconnected');
});
