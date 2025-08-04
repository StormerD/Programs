// Global variables.
var board;
var score = 0;
var rows = 4;
var columns = 4;

// Function sets the game board.
function setGame() {
  // Define game board.
  board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ];

  // Create div cells in board.
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < columns; c++) {
      // <div></div>
      let tile = document.createElement("div");
      tile.id = r.toString() + "-" + c.toString();
      let num = board[r][c];
      updateTile(tile, num);
      document.getElementById("board").append(tile);
    }
  }

  setTwo();
  setTwo();
}

// Start new game.
function newGame() {
  document.querySelectorAll('.tile').forEach(e => e.remove());
  score = 0;
  document.getElementById("score").innerText = score.toString();
  setGame();
  document.getElementById("rightSection").style.display = "none";
}

function gameOver() {

}