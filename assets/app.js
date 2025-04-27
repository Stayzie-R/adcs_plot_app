console.log("Testovací zpráva: Skript je načten");

const eventSource = new EventSource('/update_vector');

// Debugging: Ujisti se, že spojení bylo otevřeno
eventSource.onopen = function() {
    console.log("SSE spojení otevřeno");
};

// Kontrola příchozích zpráv
eventSource.onmessage = function(event) {
    console.log('Přijata zpráva:', event.data);
    const storeElement = document.getElementById('light-vector-store');
    storeElement.data = storeElement.data === true ? false : true;
    console.log('storeElement data změněna na:', storeElement.data);
};

// Kontrola chyb
eventSource.onerror = function(event) {
    console.error("Chyba při spojení s SSE:", event);
};