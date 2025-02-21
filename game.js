const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Cài đặt trạng thái game
const gameState = {
  score: 0,
  level: 1,
  rocketsFired: 0,
  maxRockets: 10,
  gameRunning: false,
};

// Khai báo các đối tượng và biến khác
let rockets = [];
const mars = { colorOverlay: { r: 255, g: 0, b: 0, alpha: 0 } };
const levelUpNotification = document.getElementById("levelUpNotification");
const gameOverNotification = document.getElementById("gameOverNotification");
const retryButton = document.getElementById("retryButton");
const exitButton = document.getElementById("exitButton");
const startScreen = document.getElementById("startScreen");

// Hàm vẽ tên lửa còn lại
function drawRemainingRockets() {
  const remaining = gameState.maxRockets - gameState.rocketsFired;
  ctx.font = "30px Arial";
  const startX = 10;
  const startY = 100;
  for (let i = 0; i < remaining; i++) {
    ctx.fillText("🚀", startX + i * 40, startY);
  }
}

// Hàm vẽ điểm số
function drawScore() {
  ctx.fillStyle = "white";
  ctx.font = "20px Arial";
  ctx.fillText(`Score: ${gameState.score}`, 10, 30);
}

// Kiểm tra level-up
function checkLevelUp() {
  if (gameState.score >= 7 && gameState.level === 1) {
    gameState.level = 2;
    levelUpNotification.style.display = "block";
    setTimeout(() => {
      levelUpNotification.style.display = "none";
    }, 3000);
  }
}

// Hàm xử lý game logic
function updateGameState() {
  checkLevelUp();
  // Thêm logic tiếp theo ở đây
  // Ví dụ: Kiểm tra các tên lửa đã bắn, các va chạm, tăng điểm...
}

// Hàm bắt đầu lại trò chơi
retryButton.addEventListener("click", () => {
  gameState.gameRunning = true;
  gameState.score = 0;
  gameState.rocketsFired = 0;
  rockets.length = 0;
  mars.colorOverlay = { r: 255, g: 0, b: 0, alpha: 0 };
  gameOverNotification.style.display = "none";
  startScreen.style.display = "none"; // Ẩn màn hình bắt đầu khi game bắt đầu
  initGame();
});

// Hàm thoát trò chơi
exitButton.addEventListener("click", () => {
  gameState.gameRunning = false;
  resetGame();
  gameOverNotification.style.display = "none";
  startScreen.style.display = "flex"; // Hiển thị màn hình bắt đầu khi thoát game
});

// Hàm khởi tạo game
function initGame() {
  // Khởi tạo lại tất cả các biến và trạng thái
  console.log("Game initialized!");
  gameState.score = 0;
  gameState.rocketsFired = 0;
  gameState.level = 1;
  mars.colorOverlay = { r: 255, g: 0, b: 0, alpha: 0 };
  gameState.maxRockets = 10; // Reset tên lửa khi bắt đầu game mới
  gameState.gameRunning = true;
  startScreen.style.display = "none"; // Ẩn màn hình bắt đầu
  gameOverNotification.style.display = "none"; // Ẩn thông báo game over
}

// Hàm reset game
function resetGame() {
  console.log("Game reset!");
  // Thực hiện reset lại khi game kết thúc
}

// Hàm xử lý logic game chính
function gameLoop() {
  if (gameState.gameRunning) {
    updateGameState();
    drawScore();
    drawRemainingRockets();
    // Thêm các logic khác của game (tên lửa bay, va chạm, v.v.)
  }

  requestAnimationFrame(gameLoop);
}

// Bắt đầu game
gameLoop();
