// cria e posiciona o mapa
const map = L.map('mapa').setView([0, 20], 2); 

// adiciona a "aparência visual" do mapa
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

async function buscarTerremotos() {
    const resposta = await fetch('http://127.0.0.1:8000/api/earthquakes/?page_size=1000');
    const dados = await resposta.json();
    console.log(dados);

    for (const terremoto of dados.results) {
        const dataFormatada = new Date(terremoto.time).toLocaleString('pt-BR');

        L.marker([terremoto.latitude, terremoto.longitude])
        .bindPopup(`<b>${terremoto.place}</b><br>Magnitude: ${terremoto.magnitude}<br>Profundidade: ${terremoto.depth} km<br>Data: ${dataFormatada}`)
        .addTo(map);
    }
}

buscarTerremotos();
