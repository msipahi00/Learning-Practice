//jshint esversion:6

const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.urlencoded({extended: true}));


app.get("/", function(req, res) {
  res.sendFile(__dirname + "/index.html");
});

app.post("/", function(req, res) {
  var sum = parseInt(req.body.num1) + parseInt(req.body.num2);
  res.send("Your answer is: " + sum);
});

app.get("/bmicalculator", function(req, res) {
  res.sendFile(__dirname + "/bmiCalculator.html");
});

app.post("/bmicalculator", function(req, res) {
  var userBMI = 703 * Number(req.body.weight) / (Number(req.body.height)^2);
  res.send("Your BMI is: " + Math.round(userBMI*10)/10);
});

app.listen("3000", function() {
  console.log("Server is running on port 3000");
});
