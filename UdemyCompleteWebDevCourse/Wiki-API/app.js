const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const mongoose = require("mongoose");
const app = express(); 
app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended:true}));

mongoose.connect('mongodb://127.0.0.1:27017/wikiDB');


const articleSchema = new mongoose.Schema({ 
    title: String, 
    content: String
});
const Article = new mongoose.model("Article", articleSchema);




app.listen(3000, function(){ 
    console.log("The server is running on port 3000")
})

// Requests targeting all articles 
app.route("/articles")
.get(function(req, res) { 
    Article.find()
    .then(articles => { 
        res.send(articles) 
    })
    .catch(err => { 
        console.log(err)
    })
})
.post(function(req, res) { 
    const article = new Article({
        title:req.body.title,
        content:req.body.content
    });
    article.save()
    .catch(err => { 
        res.send(err);
    })
    res.send("Successfully added a new article.");
})
.delete(function(req, res) { 
    Article.deleteMany()
    .catch(err => { 
        res.send(err) 
    })
    res.send("Successfully deleted articles");
});

// Requests targeting specific articles 
app.route("/articles/:articleTitle")
.get(function(req, res) { 
    Article.findOne({title:req.params.articleTitle})
    .then(foundArticle => { 
        res.send(foundArticle)
    })
    .catch(err => {
        console.log(err)
    })
})
.put(function(req, res) {
    let filter = {title:req.params.articleTitle}
    let update = {title:req.body.title, content:req.body.content}
    Article.replaceOne(filter, update)
    .then(upd => { 
        res.send("Updated Successfully");
    })
    .catch(err => { 
        res.send(err)
    })
})
.patch(function(req, res) { 
    let filter = {title:req.params.articleTitle}
    let update = {title:req.body.title, content:req.body.content}

    Article.findOneAndUpdate(filter, update, {new:true})
    .then(upd => { 
        res.send("Successfully Updated")
    })
    .catch(err => { 
        res.send(err)
    })
})
.delete(function(req, res){
    Article.deleteOne({title:req.params.articleTitle})
    .then(upd => { 
        res.send("Deleted Successfully")
    })
    .catch(err => { 
        res.send(err)
    })
})