

for (i=0;i<document.querySelectorAll(".drum").length; i++) {
    /*looping through all the drum indices*/
    /*adding event listener for each button*/
    /*logging 'this' which is the object that is being clicked*/ 

    document.querySelectorAll(".drum")[i].addEventListener("click", function () { 
        this.style.color = "white";

    });
}
