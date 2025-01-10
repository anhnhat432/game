import pygame
import sys
import math

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ trò chơi
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TR0 CHOI TAM GIAC VUONG TRON")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Font chữ
FONT = pygame.font.SysFont("Arial", 30)

# Định nghĩa các trạng thái màn hình
MENU = 'menu'
INTRO = 'intro'
MAIN = 'main'
EXIT = 'exit'

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
        self.points = points  # Danh sách các điểm của tam giác [(x1,y1), (x2,y2), (x3,y3)]
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
            self.points = [(x + self.vx, y) for (x, y) in self.points]
        if min_y <= 0 or max_y >= HEIGHT:
            self.vy *= -1
            self.points = [(x, y + self.vy) for (x, y) in self.points]

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.points)

# Hàm kiểm tra va chạm giữa hai hình tròn
def check_circle_collision(circle1, circle2):
    dist = math.hypot(circle1.x - circle2.x, circle1.y - circle2.y)
    return dist <= (circle1.radius + circle2.radius)

# Hàm kiểm tra va chạm giữa hình tròn và tam giác (đơn giản: kiểm tra xem tâm hình tròn có nằm trong tam giác không)
def point_in_triangle(pt, tri):
    # Sử dụng công thức barycentric
    (x, y) = pt
    (x1, y1), (x2, y2), (x3, y3) = tri

    denom = ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
    if denom == 0:
        return False  # Tam giác không hợp lệ
    a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / denom
    b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / denom
    c = 1 - a - b
    return 0 <= a <=1 and 0 <= b <=1 and 0 <= c <=1

def point_to_segment_distance(pt, p1, p2):
    # Tính khoảng cách từ điểm pt đến đoạn thẳng p1-p2
    x, y = pt
    x1, y1 = p1
    x2, y2 = p2

    A = x - x1
    B = y - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D
    param = -1
    if len_sq != 0:
        param = dot / len_sq

    if param < 0:
        xx, yy = x1, y1
    elif param > 1:
        xx, yy = x2, y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D

    dx = x - xx
    dy = y - yy
    return math.hypot(dx, dy)

def check_circle_triangle_collision(circle, triangle):
    # Kiểm tra xem tâm hình tròn có nằm trong tam giác không
    if point_in_triangle((circle.x, circle.y), triangle.points):
        return True
    # Kiểm tra khoảng cách từ tâm hình tròn đến từng cạnh tam giác
    for i in range(3):
        p1 = triangle.points[i]
        p2 = triangle.points[(i+1)%3]
        # Tính khoảng cách từ điểm (circle.x, circle.y) đến đoạn thẳng p1-p2
        distance = point_to_segment_distance((circle.x, circle.y), p1, p2)
        if distance <= circle.radius:
            return True
    return False

# Tạo các đối tượng hình tròn và tam giác
circle1 = Circle(x=100, y=100, radius=30, color=RED, velocity=(3, 2))
circle2 = Circle(x=700, y=500, radius=40, color=BLUE, velocity=(-2, -3))
triangle = Triangle(points=[(400, 300), (450, 350), (350, 350)], color=GREEN, velocity=(2, 2))

# Tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60

# Trạng thái hiện tại
current_state = MENU

# Hàm vẽ Menu
def draw_menu():
    screen.fill(WHITE)
    title_text = FONT.render("Chào Mừng Đến Với Trò Chơi!", True, BLACK)
    start_text = FONT.render("Nhấn ENTER để Bắt Đầu", True, BLACK)
    quit_text = FONT.render("Nhấn ESC để Thoát", True, BLACK)

    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 40))

# Hàm vẽ Intro
def draw_intro():
    screen.fill(WHITE)
    intro_lines = [
        "Đây là phần giới thiệu về trò chơi.",
        "Trò chơi gồm hai hình tròn và một tam giác.",
        "Họ sẽ di chuyển và va chạm với nhau.",
        "Chúc bạn chơi vui vẻ!",
        "Nhấn ENTER để vào Trò Chơi hoặc ESC để Quay Lại Menu."
    ]
    for idx, line in enumerate(intro_lines):
        intro_text = FONT.render(line, True, BLACK)
        screen.blit(intro_text, (50, 100 + idx * 40))

# Hàm vẽ Main Screen
def draw_main():
    screen.fill(WHITE)
    # Vẽ các hình
    circle1.draw(screen)
    circle2.draw(screen)
    triangle.draw(screen)

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
        # Di chuyển các hình
        circle1.move()
        circle2.move()
        triangle.move()

        # Kiểm tra va chạm giữa hai hình tròn
        if check_circle_collision(circle1, circle2):
            # Phản xạ vận tốc khi va chạm
            circle1.vx, circle1.vy = -circle1.vx, -circle1.vy
            circle2.vx, circle2.vy = -circle2.vx, -circle2.vy

        # Kiểm tra va chạm giữa hình tròn và tam giác
        if check_circle_triangle_collision(circle1, triangle):
            circle1.vx, circle1.vy = -circle1.vx, -circle1.vy
        if check_circle_triangle_collision(circle2, triangle):
            circle2.vx, circle2.vy = -circle2.vx, -circle2.vy

        draw_main()

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()
