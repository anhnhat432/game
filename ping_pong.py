import pygame
import sys
import math
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ trò chơi
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRÒ CHƠI NHIỀU HÌNH TRÒN")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 165, 0)]

# Font chữ
FONT = pygame.font.SysFont("Arial", 30)

# Định nghĩa các trạng thái màn hình
MENU = "menu"
INTRO = "intro"
MAIN = "main"

# Lớp Circle
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

# Hàm xử lý va chạm giữa hình tròn di chuyển và hình tròn cố định
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

# Hàm vẽ Menu
def draw_menu():
    screen.fill(WHITE)
    title_text = FONT.render("Chào Mừng Đến Với Trò Chơi!", True, BLACK)
    start_text = FONT.render("Nhấn ENTER để Bắt Đầu", True, BLACK)
    quit_text = FONT.render("Nhấn ESC để Thoát", True, BLACK)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 40))

# Hàm vẽ Intro
def draw_intro():
    screen.fill(WHITE)
    intro_lines = [
        "Đây là phần giới thiệu về trò chơi.",
        "Bạn sẽ điều khiển một màn chơi có nhiều hình tròn.",
        "Chúng di chuyển và va chạm với nhau.",
        "Nhấn ENTER để Bắt Đầu Chơi hoặc ESC để Quay Lại Menu."
    ]
    for idx, line in enumerate(intro_lines):
        intro_text = FONT.render(line, True, BLACK)
        screen.blit(intro_text, (50, 100 + idx * 40))

# Hàm vẽ Main Screen
def draw_main(fixed_circles, moving_circles):
    screen.fill(WHITE)
    for circle in fixed_circles:
        circle.draw(screen)
    for circle in moving_circles:
        circle.draw(screen)

# Tạo các đối tượng
fixed_circle1 = Circle(x=50, y=HEIGHT - 50, radius=40, color=COLORS[0], velocity=(0, 0))
fixed_circle2 = Circle(x=WIDTH - 50, y=50, radius=40, color=COLORS[1], velocity=(0, 0))

moving_circles = [
    Circle(
        x=random.randint(100, WIDTH - 100),
        y=random.randint(100, HEIGHT - 100),
        radius=random.randint(20, 40),
        color=random.choice(COLORS),
        velocity=(random.randint(-3, 3), random.randint(-3, 3))
    )
    for _ in range(8)  # 8 hình tròn di chuyển
]

# Tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60

# Trạng thái hiện tại
current_state = MENU

# Vòng lặp chính của trò chơi
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_state == MENU:
                if event.key == pygame.K_RETURN:
                    current_state = INTRO
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif current_state == INTRO:
                if event.key == pygame.K_RETURN:
                    current_state = MAIN
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
            elif current_state == MAIN:
                if event.key == pygame.K_ESCAPE:
                    current_state = MENU

    # Xử lý theo trạng thái hiện tại
    if current_state == MENU:
        draw_menu()
    elif current_state == INTRO:
        draw_intro()
    elif current_state == MAIN:
        # Di chuyển các hình tròn
        for circle in moving_circles:
            circle.move()
            resolve_fixed_circle_collision(circle, fixed_circle1)
            resolve_fixed_circle_collision(circle, fixed_circle2)

        # Vẽ màn hình chính
        draw_main([fixed_circle1, fixed_circle2], moving_circles)

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()
