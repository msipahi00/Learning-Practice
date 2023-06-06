
const express = require("express");
const bodyParser = require("body-parser");
const date = require(__dirname + "/date.js");




const app = express();
app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));
app.set("view engine", "ejs");

const items = [];
const workItems = [];
const currentDate = date.getDate();

app.listen(3000, function() {
  console.log("the server is running on port 3000");
});


//Need variable for currentDate


app.get("/", function(req, res) {


  res.render("list", {
    listTitle:"To Do List",
    currentDate:currentDate,
    newListItems:items
  });
});


app.post("/", function(req, res) {

  if (req.body.name == "Work"){
    workItems.push(req.body.newItem);
    res.redirect("/work");
  }
  else {
    items.push(req.body.newItem);
    res.redirect("/");

  }

});


app.get("/work", function(req, res) {
  res.render("list", {
    listTitle:"Work List",
    newListItems:workItems,
    currentDate: currentDate
  });

});


app.get("/about", function(req, res) {
  res.render("about");
});
