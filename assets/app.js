console.log("Testovací zpráva: Skript je načten");

const eventSource = new EventSource('/update_vector');
eventSource.onmessage = function(event) {
    console.log('Přijata zpráva:', event.data);

    const storeElement = document.getElementById('light-vector-store');
    storeElement.data = storeElement.data === true ? false : true;
    console.log('storeElement data změněna na:', storeElement.data);
};