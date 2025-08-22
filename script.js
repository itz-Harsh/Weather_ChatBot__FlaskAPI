async function fetchdata(){
    const city = document.getElementById('cityInput').value;
    console.log(city);
    if (!city) {
        alert('Please enter a city name.');
        return;
    }
    try{
        const response = await fetch(`http://127.0.0.1:5000/weather?city=`+city);
        const data = await response.json();

             document.getElementById('city').innerHTML =  `🌤️ Weather in ${data.city}: ${data.description}<br>`
             document.getElementById('temp').innerHTML =  `🌡️ Temperature: ${data.temperature}°C<br>`
             document.getElementById('humidity').innerHTML =  `💧 Humidity: ${data.humidity}%<br>`
             document.getElementById('wind').innerHTML =  `🌬️ Wind Speed: ${data.wind_speed} m/s`;

    }
    catch (error) {
    document.getElementById("responseBox").innerHTML = "❌ Error connecting to server!";
  }
}