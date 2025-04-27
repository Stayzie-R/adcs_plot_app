fetch('/update_vector', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        light_vector: your_light_vector,
        sensors: your_sensors_data
    }),
})
.then(response => {
    console.log('Odpověď serveru přijatá:', response);
    return response.json();  // Převede odpověď na JSON
})
.then(data => {
    console.log('Data přijatá ze serveru:', data);

    const storeElement = document.getElementById('light-vector-store');
    storeElement.data = data;  // Nastavuje data do dcc.Store

    console.log('Data byla uložena do dcc.Store:', storeElement.data);  // Loguj uložení
})
.catch(error => {
    console.error('Chyba při odesílání požadavku:', error);
});
