var map = L.map('map').setView([51.505, -0.09], 13);

// ajout un OpenStreetMap tuile de carte
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// ajoute un marqueur dans une position donné, définit un contenu au marqueur et crée le popup 
L.marker([51.5, -0.09]).addTo(map)
    .bindPopup('A pretty CSS3 popup. <br> Easily customizable.')
    .openPopup();
