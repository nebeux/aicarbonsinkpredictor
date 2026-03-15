// things to finish before 10am tmrw
// add loading screen during fetch
// display actual info
// if i have time, finish adding an input so they can type in their own coords.


// init map
var map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

var marker;

map.on('click', function(e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;

    // move marker to clicked spot (idk gng im doing ts straight from documentation :sob:)
    if (marker) {
        marker.setLatLng(e.latlng);
    } else {
        marker = L.marker(e.latlng).addTo(map);
    }
    console.log(lat,lng)
    gofetch(lat,lng)

})
function gofetch(lat,lng){
    switchBodyToLoad()
fetch('/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lat: lat, lng: lng })
})
.then(res => res.json())
.then(data => {
    switchLoadtoBody()
    console.log(data.prediction) 
    if (data.prediction == "670notinwater"){
        console.log("P")
        panicMode()
    }else if (data.extra_info == "fallback"){
        console.log("F")
        nofallback(data)
    }else{
        console.log("NF")
        nofallback(data)
    }
})
}
function panicMode() {
    document.body.style.transition = 'background 0.1s';
    let blinks = 0;
    const blink = setInterval(() => {
        document.body.style.background = blinks % 2 === 0 ? '#ff000033' : 'transparent';
        blinks++;
        document.getElementById('randomh1').textContent = ""
        if (blinks > 10) {
            clearInterval(blink);
            document.body.style.background = '';
            const wrapper = document.getElementById('results-wrapper');
            wrapper.innerHTML = `
        <div style="
            background: rgba(0,200,255,0.05);
            border: 1px solid rgba(0,200,255,0.2);
            border-radius: 12px;
            padding: 24px;
            color: white;
            max-width: 400px;">

            <h2 style="margin:0 0 8px; font-size:40px; color:red">
                N/A<span style="font-size:16px; opacity:0.6">/(N/A)</span>
            </h2>
            <p style="margin:0 0 16px; color:red; font-size:14px; letter-spacing:1px;">
                Choose a valid oceanic coordinate!
            </p>

            <hr style="border-color: rgba(0,200,255,0.1); margin-bottom:16px;">

            <div style="font-size:13px; opacity:0.7; line-height:2;">
                <div>🌡️ Sea Temp: <b>N/A°C</b></div>
                <div>🌿 Chlorophyll: <b>N/A mg/m³</b></div>
                <div>💧 Salinity: <b>N/A PSU</b></div>
                <div>💨 Wind Speed: <b>N/A m/s</b></div>
            </div>

            <hr style="border-color: rgba(0,200,255,0.1); margin: 16px 0;">

            <p style="font-size:12px; opacity:0.5; margin:0;">
               Choose a valid oceanic coordinate!
            </p>
        </div>
    `;

        }
    }, 100);

    document.body.style.animation = 'shake 0.5s ease';
    setTimeout(() => document.body.style.animation = '', 500);
}

function switchBodyToLoad(){
document.getElementById("loading-screen").style.display = "flex"
}
function switchLoadtoBody(){
document.getElementById("loading-screen").style.display = "none"
}


function nofallback(data){
    const score = data.prediction.toFixed(2);
    const wrapper = document.getElementById('results-wrapper');

    let label, color;
    if (score <= 30) { label = "Poor carbon absorption region"; color = "#ff4444"; }
    else if (score <= 60) { label = "Moderate carbon absorption region"; color = "#ffaa00"; }
    else if (score <= 80) { label = "Good carbon absorption region"; color = "#00cc66"; }
    else { label = "Excellent carbon absorption region"; color = "#00c8ff"; }

    let reason = "";
    if (data.chlorophyll > 4) reason += "High chlorophyll indicates strong phytoplankton activity. ";
    else if (data.chlorophyll < 2) reason += "Low chlorophyll limits biological carbon uptake. ";
    if (data.sea_temp < 10) reason += "Cold water enhances CO₂ solubility. ";
    else if (data.sea_temp > 22) reason += "Warm water reduces CO₂ absorption capacity. ";
    if (!reason) reason = "Moderate oceanic conditions detected.";

    wrapper.innerHTML = `
        <div style="
            background: rgba(0,200,255,0.05);
            border: 1px solid rgba(0,200,255,0.2);
            border-radius: 12px;
            padding: 24px;
            color: white;
            max-width: 400px;">

            <h2 style="margin:0 0 8px; font-size:40px; color:${color}">
                ${score}<span style="font-size:16px; opacity:0.6">/100</span>
            </h2>
            <p style="margin:0 0 16px; color:${color}; font-size:14px; letter-spacing:1px;">
                ${label}
            </p>

            <hr style="border-color: rgba(0,200,255,0.1); margin-bottom:16px;">

            <div style="font-size:13px; opacity:0.7; line-height:2;">
                <div>🌡️ Sea Temp: <b>${data.sea_temp.toFixed(1)}°C</b></div>
                <div>🌿 Chlorophyll: <b>${data.chlorophyll.toFixed(2)} mg/m³</b></div>
                <div>💧 Salinity: <b>${data.salinity.toFixed(1)} PSU</b></div>
                <div>💨 Wind Speed: <b>${data.wind_speed.toFixed(1)} m/s</b></div>
            </div>

            <hr style="border-color: rgba(0,200,255,0.1); margin: 16px 0;">

            <p style="font-size:12px; opacity:0.5; margin:0;">
                ${reason}
            </p>
        </div>
    `;
    
    
}