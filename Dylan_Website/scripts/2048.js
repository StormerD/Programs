// global variables
var board;
var score = 0;
var rows = 4;
var columns = 4;

// function sets the board
function setGame() {
    // defines game board
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    // creates div cells in board
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

// starts new game
function newGame() {
    document.querySelectorAll('.tile').forEach(e => e.remove());
    score = 0;
    document.getElementById("score").innerText = score.toString();
    setGame();
    document.getElementById("rightSection").style.display = "none";
}

function gameOver() {
    document.getElementById("rightSection").style.display = "block";
}

function checkCanSlide(row) {
    row = filterZero(row);

    // check pairs
    for(let i = 0; i < row.length - 1; i++) {
        // check every pair
        if (row[i] == row[i + 1]) {
            return true;
        }
    }
    return false
}

function checkGameOver() {
    let gOver = true;
    for(let r = 0; r < rows; r++) {
        let row = board[r]
        if (checkCanSlide(row)) {
            gOver = false;
        }
    }
    for(let c = 0; c < columns; c++) {
        let row = [board[0][c], board[1][c], board[2][c], board[3][c]];
        if (checkCanSlide(row)) {
            gOver = false;
        }
    }
    if (gOver == true) {
        gameOver();
    }
    return;
}

// checks if board has any empty tiles
function hasEmptyTile() {
    for(let r = 0; r < rows; r++) {
        for(let c = 0; c < columns; c++) {
            if (board[r][c] == 0) {
                return true;
            }
        }
    }
    return false;
}

// adds 2 tile on random square
function setTwo() {
    if (!hasEmptyTile()) {
        checkGameOver();
        return;
    }
    
    let found = false;
    while(!found) {
        let r = Math.floor(Math.random() * rows);
        let c = Math.floor(Math.random() * columns);
        
        if (board[r][c] == 0) {
            board[r][c] = 2;
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            tile.innerText = "2";
            tile.classList.add("x2");
            found = true;
        }
    }
    
    if (!hasEmptyTile()) {
        checkGameOver();
        return;
    }
}

// function updates the tile into correct pos
function updateTile(tile, num) {
    tile.innerText = ""; // clear text
    tile.classList.value = ""; // clear classList
    tile.classList.add("tile");
    if (num > 0) {
        tile.innerText = num.toString();
        if (num <= 4096) {
            tile.classList.add("x" + num.toString());
        }
        else {
            tile.classList.add("x8192");
        }
    }
}

// function defines key actions
document.addEventListener("keyup", (e) => {
    if (e.code === "ArrowUp") {
        slideUp();
        setTwo();
    }
    else if (e.code === "ArrowLeft") {
        slideLeft();
        setTwo();
    }
    else if (e.code === "ArrowDown") {
        slideDown();
        setTwo();
    }
    else if (e.code === "ArrowRight") {
        slideRight();
        setTwo();
    }
    document.getElementById("score").innerText = score.toString();
})

function filterZero(row) {
    // creates new array without 0s
    return row.filter(num => num != 0); 
}

function slide(row) {
    // filter out 0s
    row = filterZero(row);
    
    // slide
    for(let i = 0; i < row.length - 1; i++) {
        // check every pair
        if (row[i] == row[i + 1]) {
            row[i] *= 2;
            row[i + 1] = 0;
            score += row[i];
        }
    }

    // filter out 0s
    row = filterZero(row);

    // add 0s back
    while(row.length < columns) {
        row.push(0);
    }

    return row;
}

function slideUp() {
    for(let c = 0; c < columns; c++) {
        let row = [board[0][c], board[1][c], board[2][c], board[3][c]];
        row = slide(row);
        board[0][c] = row[0];
        board[1][c] = row[1];
        board[2][c] = row[2];
        board[3][c] = row[3];
        for(let r = 0; r < rows; r++) {
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c]
            updateTile(tile, num);
        }
    }
}

function slideLeft() {
    for(let r = 0; r < rows; r++) {
        let row = board[r];
        row = slide(row);
        board[r] = row;
        for(let c = 0; c < columns; c++) {
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c]
            updateTile(tile, num);
        }
    }
}

function slideDown() {
    for(let c = 0; c < columns; c++) {
        let row = [board[0][c], board[1][c], board[2][c], board[3][c]];
        row.reverse();
        row = slide(row);
        row.reverse();
        board[0][c] = row[0];
        board[1][c] = row[1];
        board[2][c] = row[2];
        board[3][c] = row[3];
        for(let r = 0; r < rows; r++) {
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c]
            updateTile(tile, num);
        }
    }
}

function slideRight() {
    for(let r = 0; r < rows; r++) {
        let row = board[r];
        row.reverse();
        row = slide(row);
        row.reverse();
        board[r] = row;
        for(let c = 0; c < columns; c++) {
            let tile = document.getElementById(r.toString() + "-" + c.toString());
            let num = board[r][c]
            updateTile(tile, num);
        }
    }
}

// sets the board on window load
window.onload = function() {
    setGame();
}