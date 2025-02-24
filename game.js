// game.js
class Rocket {
  constructor(x, y, directionX, directionY) {
    this.x = x;
    this.y = y;
    this.directionX = directionX;
    this.directionY = directionY;
    this.baseSpeed = 3;
    this.width = 10;
    this.height = 20;
    this.vx = this.directionX * this.baseSpeed;
    this.vy = this.directionY * this.baseSpeed;
  }

  calculateSpeed() {
    const dx = this.x - earth.x,
      dy = this.y - earth.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    const minSpeed = 0.3,
      maxDistance = 800;
    return Math.max(minSpeed, this.baseSpeed * (1 - distance / maxDistance));
  }

  move() {
    const speed = this.calculateSpeed();
    this.vx = this.directionX * speed * 0.8;
    this.vy = this.directionY * speed * 0.8;
    this.x += this.vx;
    this.y += this.vy;
  }

  draw(ctx) {
    const angle = Math.atan2(this.vy, this.vx);
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(angle);
    ctx.fillStyle = "white";
    ctx.fillRect(0, -this.height / 2, this.width, this.height);
    ctx.beginPath();
    ctx.moveTo(this.width, -this.height / 2);
    ctx.lineTo(this.width, this.height / 2);
    ctx.lineTo(this.width + this.width / 2, 0);
    ctx.closePath();
    ctx.fillStyle = "red";
    ctx.fill();
    ctx.fillStyle = "blue";
    ctx.beginPath();
    ctx.arc(this.width / 2, 0, this.height / 8, 0, Math.PI * 2);
    ctx.fill();
    const flameGradient = ctx.createLinearGradient(
      -this.width / 2,
      0,
      -this.width * 2,
      0
    );
    flameGradient.addColorStop(0, "yellow");
    flameGradient.addColorStop(0.5, "orange");
    flameGradient.addColorStop(1, "red");
    ctx.fillStyle = flameGradient;
    ctx.beginPath();
    ctx.moveTo(-this.width / 2, -this.height / 4);
    ctx.lineTo(-this.width * 2, 0);
    ctx.lineTo(-this.width / 2, this.height / 4);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "gray";
    ctx.beginPath();
    ctx.moveTo(0, -this.height / 2);
    ctx.lineTo(-this.width / 2, -this.height / 4);
    ctx.lineTo(0, 0);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(0, this.height / 2);
    ctx.lineTo(-this.width / 2, this.height / 4);
    ctx.lineTo(0, 0);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  hasReachedTarget() {
    if (
      this.x < -this.width ||
      this.x > canvas.width + this.width ||
      this.y < -this.height ||
      this.y > canvas.height + this.height
    ) {
      return true;
    }
    const dx = this.x - mars.x,
      dy = this.y - mars.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    return distance < mars.radius;
  }
}

class Game {
  constructor(canvas, ctx) {
    this.canvas = canvas;
    this.ctx = ctx;
    this.score = 0;
    this.level = 1;
    this.rocketsFired = 0;
    this.maxRockets = 10;
    this.rockets = [];
    this.isGameRunning = false;

    this.earth = {
      x: 150,
      y: canvas.height - 150,
      radius: 120,
      image: new Image(),
    };
    this.earth.image.src =
      "https://i.postimg.cc/vHdpQfXm/Pngtree-earth-globe-vector-design-19771842.png";

    this.mars = {
      x: canvas.width - 150,
      y: 150,
      radius: 80,
      vx: 0.5,
      vy: 0.3,
      colorOverlay: { r: 255, g: 0, b: 0, alpha: 0 },
      image: new Image(),
    };
    this.mars.image.src =
      "https://i.postimg.cc/MTCgfQSd/Pngtree-night-sky-planet-mars-universe-4523018.png";
  }

  resetGame() {
    this.score = 0;
    this.level = 1;
    this.rocketsFired = 0;
    this.rockets = [];
    this.mars.colorOverlay = { r: 255, g: 0, b: 0, alpha: 0 };
  }

  update() {
    if (!this.isGameRunning) return;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.ctx.fillStyle = "#222"; // Hoặc vẽ hình nền khác
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.drawEarth();
    this.drawMars();

    this.rockets.forEach((rocket, index) => {
      rocket.move();
      rocket.draw(this.ctx);
      if (rocket.hasReachedTarget()) {
        this.rockets.splice(index, 1);
        const dx = rocket.x - this.mars.x;
        const dy = rocket.y - this.mars.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < this.mars.radius) {
          this.score += 1;
          this.mars.changeColor();
        }
      }
    });
  }

  drawEarth() {
    this.ctx.save();
    this.ctx.beginPath();
    this.ctx.arc(this.earth.x, this.earth.y, this.earth.radius, 0, Math.PI * 2);
    this.ctx.closePath();
    this.ctx.clip();
    this.ctx.drawImage(
      this.earth.image,
      this.earth.x - this.earth.radius,
      this.earth.y - this.earth.radius,
      this.earth.radius * 2,
      this.earth.radius * 2
    );
    this.ctx.restore();
  }

  drawMars() {
    this.ctx.save();
    this.ctx.beginPath();
    this.ctx.arc(this.mars.x, this.mars.y, this.mars.radius, 0, Math.PI * 2);
    this.ctx.closePath();
    this.ctx.clip();
    this.ctx.drawImage(
      this.mars.image,
      this.mars.x - this.mars.radius,
      this.mars.y - this.mars.radius,
      this.mars.radius * 2,
      this.mars.radius * 2
    );
    if (this.mars.colorOverlay.alpha > 0) {
      this.ctx.beginPath();
      this.ctx.arc(this.mars.x, this.mars.y, this.mars.radius, 0, Math.PI * 2);
      this.ctx.closePath();
      this.ctx.globalCompositeOperation = "source-atop";
      this.ctx.fillStyle = `rgba(${this.mars.colorOverlay.r}, ${this.mars.colorOverlay.g}, ${this.mars.colorOverlay.b}, ${this.mars.colorOverlay.alpha})`;
      this.ctx.fill();
    }
    this.ctx.restore();
  }

  handleLevelUp() {
    if (this.score >= 7 && this.level === 1) {
      this.level = 2;
      this.resetGame(); // Đảm bảo reset lại trạng thái game sau khi qua màn
      levelUpNotification.style.display = "none"; // Ẩn thông báo qua màn
      continueLevelNotification.style.display = "block"; // Hiển thị thông báo yêu cầu xác nhận tiếp tục
    }
  }
}

export { Game }; // Xuất lớp Game để sử dụng ở các file khác
