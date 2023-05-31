buttonColors = ["red", "purple", "green", "yellow"];
gamePattern = [];
userClickedPattern = [];
started = false; 
var level = 0; 
highScore = 0; 



if (started == false){
  $("*").on("keypress", function() {
    started = true;
    nextSequence();  
    $("*").off("keypress");
  });
}


function nextSequence() {
  level ++;
  $("#level-title").text("Level " + level);
  var randomNumber = Math.floor(Math.random()*4);
  console.log(randomNumber);
  var randomChosenColor = buttonColors[randomNumber];
  gamePattern.push(randomChosenColor);

  playSound(randomChosenColor);
  animatePress(randomChosenColor);

}

$(".btn").on("click", function() { 
  var userChosenColor = this.id; 
  userClickedPattern.push(userChosenColor); 
  console.log(userClickedPattern);
  playSound(userChosenColor);
  animatePress(userChosenColor);
  checkAnswer(userClickedPattern.length-1); /* INDEX OF LAST SEQUENCE*/
})


function playSound(name) { 
  var sound = new Audio("./sounds/"+name+".mp3");
  sound.play(); 
}

function animatePress(name) { 
  $("."+name).addClass("pressed");
  setTimeout( function() { 
    $("."+name).removeClass("pressed");
  }, 200)
}


function checkAnswer(currentLevel) { 
  if (userClickedPattern[currentLevel] == gamePattern[currentLevel]){
    console.log("success");
    if (userClickedPattern.length == level){
      setTimeout( function() { 
        userClickedPattern.length = 0;
        nextSequence();
      }, 1000);
    }
  }
  else{ 
    console.log("wrong");
    let incorrect = new Audio("./sounds/wrong.mp3");
    incorrect.play(); 
    $("*").addClass("game-over");
    setTimeout( function() { 
      $("*").removeClass("game-over");
    }, 200);
    $("h1").text("Game Over, Press Any Key to Try Again");
    startOver(); 
  }
}

function startOver() {
  if (level-1 > highScore){
    highScore = level-1;
  }  
  $("h2").text("High Score: " + highScore);
  level = 0; 
  gamePattern.length = 0; 
  started = false; 
  
}