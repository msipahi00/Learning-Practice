const fs = require("fs");
/*short for filesystem*/
/*want to take a message that a user inputs to write into a file and save on the computer*/

fs.writeFile("message.txt", "Hello from NodeJS", (err) => {
    if (err) throw err;
    console.log("This file has been saved!");
});

fs.readFile("./message.txt","utf8", (err, data)=> { 
    if (err) throw err;
    console.log(data);
});