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
.then(response => response.json())
.then(data => {
    const storeElement = document.getElementById('light-vector-store');
    storeElement.data = data; 
})
.catch(error => console.error('Error:', error));