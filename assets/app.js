console.log("Testovací zpráva: Skript je načten");

const eventSource = new EventSource('/stream');

eventSource.onopen = function() {
    console.log("SSE spojení otevřeno");
};

eventSource.onmessage = function(event) {
    console.log("Přijata zpráva:", event.data);
    
};

eventSource.onerror = function(event) {
    console.error("Chyba při SSE spojení:", event);
};
