

for (i=0;i<document.querySelectorAll(".drum").length; i++) {
    /*looping through all the drum indices*/
    /*adding event listener for each button*/
    /*logging 'this' which is the object that is being clicked*/ 
    /*logging clicks*/

    document.querySelectorAll(".drum")[i].addEventListener("click", function () { 
        
        var buttonInnerHTML = this.innerHTML;
        makeSound(buttonInnerHTML);
        buttonAnimation(buttonInnerHTML);
    });
}


/*logging keyboard presses */
document.addEventListener("keypress", function(event) {
    makeSound(event.key);
    buttonAnimation(event.key);
})

function makeSound(key) {
    switch (key) { 
        case "w": 
        var crash = new Audio("./sounds/crash.mp3");
        crash.play();
        break;

        case "a":
        var kick = new Audio("./sounds/kick-bass.mp3");
        kick.play();
        break;

        case "s":
        var snare = new Audio("./sounds/snare.mp3");
        snare.play()
        break;

        case "d":
        var tom1 = new Audio("./sounds/tom-1.mp3");
        tom1.play();
        break;

        case "j":
        var tom2 = new Audio("./sounds/tom-2.mp3");
        tom2.play();
        break;

        case "k":
        var tom3 = new Audio("./sounds/tom-3.mp3");
        tom3.play();
        break;

        case "l":
        var tom4 = new Audio("./sounds/tom-4.mp3");
        tom4.play();
        break;

        default: console.log()

    }
}


function buttonAnimation(currentKey) {

    var activeButton = document.querySelector("." + currentKey);
    /*create variable to select the object that will be manipulated*/
    activeButton.classList.add("pressed");
    /*add the pressed class to the button*/
    
    /*set the timeout for the button. First create a function that removes the pressed class from the button
    Second, wait 0.1s (100 milliseconds) for the function to be called */
    setTimeout(function() {
        activeButton.classList.remove("pressed");
    }, 100);

}
