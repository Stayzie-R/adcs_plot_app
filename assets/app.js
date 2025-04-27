console.log("Testovací zpráva: Skript je načten");

const eventSource = new EventSource('/update_vector');

eventSource.onopen = function() {
    console.log("SSE spojení otevřeno");
};

eventSource.onmessage = function(event) {
    console.log('Přijata zpráva:', JSON.parse(event.data));
};

eventSource.onerror = function(event) {
    console.error("Chyba při spojení s SSE:", event);
};