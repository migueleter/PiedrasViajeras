let map; // Variable global para el mapa
let marker; // Variable global para el marcador

// Función que se llama cuando la API de Google Maps está lista
function initMap() {
    const defaultLocation = { lat: -34.397, lng: 150.644 }; // Ejemplo: Australia
    map = new google.maps.Map(document.getElementById("map"), {
        center: defaultLocation,
        zoom: 8,
    });
    // Puedes añadir un marcador inicial si lo deseas
    marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        title: "Ubicación inicial"
    });
}

document.getElementById('getLocationButton').addEventListener('click', () => {
    const status = document.getElementById('locationStatus');
    status.textContent = 'Solicitando ubicación...';

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                status.textContent = `Tu ubicación: Latitud ${userLocation.lat}, Longitud ${userLocation.lng}`;
                
                // Centrar el mapa en la ubicación del usuario
                map.setCenter(userLocation);
                map.setZoom(15); // Un zoom más cercano

                // Mover el marcador a la nueva ubicación
                if (marker) {
                    marker.setPosition(userLocation);
                } else {
                    marker = new google.maps.Marker({
                        position: userLocation,
                        map: map,
                        title: "Tu ubicación"
                    });
                }
            },
            (error) => {
                let errorMessage;
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = "Acceso a la ubicación denegado por el usuario.";
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = "Información de ubicación no disponible.";
                        break;
                    case error.TIMEOUT:
                        errorMessage = "La solicitud para obtener la ubicación ha caducado.";
                        break;
                    default:
                        errorMessage = "Ocurrió un error desconocido al obtener la ubicación.";
                }
                status.textContent = `Error: ${errorMessage}`;
                console.error("Error al obtener la ubicación:", error);
            }
        );
    } else {
        status.textContent = "Tu navegador no soporta la geolocalización.";
    }
});

// Asegúrate de que la función initMap se llame.
// Esto se hace automáticamente si cargas la API de Google Maps con &callback=initMap
// Si no, necesitarías llamarla manualmente aquí después de que el DOM esté cargado.
// window.onload = initMap; // Solo si no usas el callback en el script de la API
