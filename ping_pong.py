import pygame
import sys
import math

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ trò chơi
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRÒ CHƠI VỚI HÌNH TRÒN CỐ ĐỊNH")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Font chữ
FONT = pygame.font.SysFont("Arial", 30)

# Định nghĩa lớp Circle
class Circle:
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx, self.vy = velocity

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Kiểm tra va chạm với các cạnh cửa sổ
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.vx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# Định nghĩa lớp Triangle
class Triangle:
    def __init__(self, points, color, velocity):
        self.points = points
        self.color = color
        self.vx, self.vy = velocity

    def move(self):
        # Di chuyển tam giác theo vận tốc
        self.points = [(x + self.vx, y + self.vy) for (x, y) in self.points]

        # Kiểm tra va chạm với các cạnh cửa sổ và phản xạ
        min_x = min([p[0] for p in self.points])
        max_x = max([p[0] for p in self.points])
        min_y = min([p[1] for p in self.points])
        max_y = max([p[1] for p in self.points])

        if min_x <= 0 or max_x >= WIDTH:
            self.vx *= -1
        if min_y <= 0 or max_y >= HEIGHT:
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.points)

# Hàm xử lý va chạm giữa đối tượng di chuyển và hình tròn cố định
def resolve_fixed_circle_collision(moving_circle, fixed_circle):
    dx = moving_circle.x - fixed_circle.x
    dy = moving_circle.y - fixed_circle.y
    dist = math.hypot(dx, dy)

    if dist == 0:
        dist = 1  # Tránh chia cho 0

    overlap = moving_circle.radius + fixed_circle.radius - dist

    if overlap > 0:  # Có va chạm
        # Vector đơn vị hướng từ hình tròn cố định đến hình tròn di chuyển
        nx = dx / dist
        ny = dy / dist

        # Đẩy hình tròn di chuyển ra khỏi hình tròn cố định
        moving_circle.x += nx * overlap
        moving_circle.y += ny * overlap

        # Phản xạ vận tốc của hình tròn di chuyển
        dot_product = moving_circle.vx * nx + moving_circle.vy * ny
        moving_circle.vx -= 2 * dot_product * nx
        moving_circle.vy -= 2 * dot_product * ny

# Hàm xử lý va chạm giữa tam giác và hình tròn cố định
def resolve_triangle_circle_collision(triangle, fixed_circle):
    for point in triangle.points:  # Lặp qua các đỉnh của tam giác
        dx = point[0] - fixed_circle.x
        dy = point[1] - fixed_circle.y
        dist = math.hypot(dx, dy)

        if dist <= fixed_circle.radius:  # Kiểm tra va chạm
            # Vector đơn vị hướng từ tâm hình tròn đến đỉnh tam giác
            nx = dx / dist
            ny = dy / dist

            # Đẩy tam giác ra khỏi hình tròn
            overlap = fixed_circle.radius - dist
            triangle.points = [
                (x + nx * overlap, y + ny * overlap) if (x, y) == point else (x, y)
                for x, y in triangle.points
            ]

            # Phản xạ vận tốc của tam giác
            dot_product = triangle.vx * nx + triangle.vy * ny
            triangle.vx -= 2 * dot_product * nx
            triangle.vy -= 2 * dot_product * ny

# Tạo các đối tượng
fixed_circle1 = Circle(x=50, y=HEIGHT - 50, radius=40, color=RED, velocity=(0, 0))  # Góc trái dưới
fixed_circle2 = Circle(x=WIDTH - 50, y=50, radius=40, color=BLUE, velocity=(0, 0))  # Góc phải trên
moving_circle = Circle(x=400, y=300, radius=30, color=GREEN, velocity=(3, 3))  # Hình tròn di chuyển
triangle = Triangle(points=[(300, 200), (350, 250), (250, 250)], color=BLACK, velocity=(2, 2))

# Tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60

# Vòng lặp chính của trò chơi
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Di chuyển các đối tượng
    moving_circle.move()
    triangle.move()

    # Xử lý va chạm
    resolve_fixed_circle_collision(moving_circle, fixed_circle1)
    resolve_fixed_circle_collision(moving_circle, fixed_circle2)
    resolve_triangle_circle_collision(triangle, fixed_circle1)
    resolve_triangle_circle_collision(triangle, fixed_circle2)

    # Vẽ tất cả đối tượng
    screen.fill(WHITE)
    fixed_circle1.draw(screen)
    fixed_circle2.draw(screen)
    moving_circle.draw(screen)
    triangle.draw(screen)

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()
