
const express = require("express");
const bodyParser = require("body-parser");
const date = require(__dirname + "/date.js");
const _ = require("lodash");

const mongoose = require("mongoose");

mongoose.connect('mongodb+srv://admin-mark:Test123@cluster0.jubfqy0.mongodb.net/toDoListDB')
.then( upd => {
  console.log("MongoDatabase has been created");
})
.catch (err => {
  console.log(err);
})



const currentDate = date.getDate();

const itemSchema = new mongoose.Schema({
  name: String
});

const listSchema = new mongoose.Schema({ 
  name: String, 
  items:[itemSchema]
});

const List = new mongoose.model("List", listSchema);

const Item = new mongoose.model("Item", itemSchema);

const firstItem = new Item({
  name: "MyFirstItem"
});
const secondItem = new Item({
  name: "MySecondItem"
});
const thirdItem = new Item({
  name: "MyThirdItem"
});





const app = express();
app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));
app.set("view engine", "ejs");





app.listen(3000 || process.env.PORT, function() {
  console.log("Server is running successfully.");
});




app.get("/", function(req, res) {



  Item.find()
  .then(items => { 
    if (items.length == 0){
      Item.insertMany([firstItem, secondItem, thirdItem]);
      res.redirect("/");
    }
    else { 
      res.render("list", {
        listTitle:"To Do List",
        currentDate:currentDate,
        newListItems:items
      });
    } 
  })
  .catch(err => { 
    console.log(err);
  })


});


app.get("/:customListName", function(req, res) {
  var customListName = _.capitalize(req.params.customListName);
  List.findOne({name:customListName})
  .then(upd => {
    if (upd){
      console.log("exists");
      //show an existing list
      res.render("list", {
        listTitle:"To Do List: " + customListName,
        currentDate:currentDate,
        newListItems:upd.items
      });
    }
    else{
      console.log("doesn't exists")
      //create a new list
      const list = new List({ 
        name: customListName,
        items:[firstItem, secondItem, thirdItem]
      });
      list.save(); 
      res.redirect("/" + customListName);
    }
  })
  .catch(err => {
    console.log(err);
  })


});



app.post("/", function(req, res) {

  const listName = req.body.list; 
  console.log(listName);

  const newItem = new Item({
    name: req.body.newItem
  });

  if (listName == "To Do List: "){
    res.redirect("/")
    newItem.save(); 
  }
  else{ 

    let dbName = listName.split(': ')[1];
    console.log(dbName);
    List.findOne({name:dbName})
    .then(foundList => { 
      foundList.items.push(newItem);
      foundList.save();
      res.redirect("/" + dbName);
    })
    .catch(err => { 
      console.log(err);
    });
  }


});

app.post("/delete", function(req, res) { 
  const listName = req.body.listName; 
  const dbName = listName.split(": ")[1];

  if (listName == "To Do List: ") { 
    Item.deleteOne({_id:req.body.checkbox})
    .then( upd => {
      res.redirect("/");
      console.log("deleted successfully");
    })
    .catch(err => { 
      console.log(err);
    })
  }
  else { 
    let conditions = {name: dbName};
    let updates = {$pull: {items: {_id:req.body.checkbox}}};
    List.findOneAndUpdate(conditions, updates)
    .then(out => { 
      console.log("Deleting and redirecting");
      res.redirect("/" + dbName);
    })
    .catch(err => { 
      console.log(err);
    })
  }

  

})


app.get("/about", function(req, res) {
  res.render("about");
});
