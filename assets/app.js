console.log("Testovací zpráva: Skript je načten");

const eventSource = new EventSource('/update_vector');

eventSource.onopen = function() {
    console.log("SSE spojení otevřeno");
};

eventSource.onmessage = function(event) {

    const storeElement = document.getElementById('light-vector-store');
    storeElement.data = storeElement.data === true ? false : true;

    console.log('storeElement data změněna na:', storeElement.data);
};

eventSource.onerror = function(event) {
    console.error("Chyba při spojení s SSE:", event);
};