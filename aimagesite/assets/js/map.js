const latitude = 50.28856;
const longitude = 18.67750;

const zoom = 13;

var mymap = L.map('mapid').setView([latitude, longitude], zoom);


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

L.marker([latitude, longitude]).addTo(mymap)
    .bindPopup('<p>Our university<br>and faculty</p>')
    .openPopup();