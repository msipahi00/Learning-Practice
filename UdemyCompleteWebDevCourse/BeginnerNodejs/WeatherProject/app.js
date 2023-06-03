const express = require("express");
const http = require("http");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.urlencoded({extended:true}));


app.get("/", function(req, res) {
  res.sendFile(__dirname + "/index.html");

});

app.post("/", function(req, res) {
  const query = req.body.cityName;
  const apiKey = "61c1d72b3ce18d50991388d844626ec6";
  const units = "imperial";
  const url = "http://api.openweathermap.org/data/2.5/weather?q=" + query + "&units=" + units + "&APPID=" + apiKey

  http.get(url, function(response) {
    console.log("status code: " + response.statusCode);

    response.on("data", function(data) {
      const weatherData = JSON.parse(data);
      const temp = weatherData.main.temp;
      const weatherDescription = weatherData.weather[0].description;
      const imgIcon = weatherData.weather[0].icon;
      const imgURL = ("https://openweathermap.org/img/wn/" + imgIcon + "@2x.png");
      console.log(imgURL);

      console.log(temp);
      console.log(weatherDescription);

      res.write("<h1>The temperature in " + query + " is currently " + temp + " degrees Farenheight.</h1>");
      res.write("<h3> The weather is currently " + weatherDescription + ".</h3>");
      res.write("<div style='background-color: black; display:inline-block;'>");
      res.write("<img src=" + imgURL + " alt=" + weatherDescription + "/>");
      res.write("</div>");


      res.send();
      });

    });

});






app.listen("3000", function () {
console.log("The server is running on port 3000");
});


// Change from hexadecimal to readable format (JSON.parse(object))
// Change from JavaScript to String format (JSON.stringify(object))
