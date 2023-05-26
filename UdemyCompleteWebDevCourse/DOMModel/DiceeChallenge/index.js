var p1Val = Math.floor(Math.random()*6) + 1;
var p2Val = Math.floor(Math.random()*6) + 1;

if (p1Val > p2Val) {
    /*change winner to p1 */
    document.querySelector("h1").innerHTML = "Player 1 Wins!";
}
else if (p2Val > p1Val) {
    /* change winner to p2*/
    document.querySelector("h1").innerHTML = "Player 2 Wins!"
}
else {
    /*change to tie*/
    document.querySelector("h1").innerHTML = "It's a Tie!"
}

var player1Dice = "./images/dice" + p1Val + ".png";
var player2Dice = "./images/dice" + p2Val + ".png";

var player1 = document.querySelector(".p1").setAttribute("src", player1Dice);
var player2 = document.querySelector(".p2").setAttribute("src", player2Dice)


