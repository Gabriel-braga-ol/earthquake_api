const globo = Globe()
    .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    (document.getElementById('globo'));

async function buscarTerremotos() {
    const resposta = await fetch('http://127.0.0.1:8000/api/earthquakes/?page_size=1000');
    const dados = await resposta.json();

    globo
        .pointsData(dados.results)
        .pointLat('latitude')
        .pointLng('longitude')
        .pointColor(() => 'red')
        .pointAltitude(0.01);
}

buscarTerremotos();