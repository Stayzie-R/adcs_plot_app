function updateStoreWithLightVector(data) {
    let light_vector = data.light_vector;
    let store = document.getElementById('light-vector-store');
    store.data = light_vector;  // Nastavíme novou hodnotu do Store
}