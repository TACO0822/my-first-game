import pygame

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('AABB Example')

# 색상 정의
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# 사각형 클래스 정의
class Rectangle:
    def __init__(self, x, y, width, height, movable=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movable = movable  # 움직일 수 있는지 여부
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)  # 회색 사각형 그리기
        pygame.draw.rect(screen, RED, self.rect, 2)  # 빨간색 AABB (테두리) 그리기

    def move(self, dx, dy):
        if self.movable:
            self.rect.x += dx
            self.rect.y += dy

# 오브젝트 생성
movable_rect = Rectangle(100, 100, 50, 50, movable=True)  # 움직일 수 있는 사각형
fixed_rect = Rectangle(375, 275, 50, 50)  # 화면 중앙에 고정된 사각형

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -5
    if keys[pygame.K_RIGHT]:
        dx = 5
    if keys[pygame.K_UP]:
        dy = -5
    if keys[pygame.K_DOWN]:
        dy = 5

    # 움직일 수 있는 사각형 이동
    movable_rect.move(dx, dy)

    # 화면에 그리기
    screen.fill((0, 0, 0))  # 화면을 검정색으로 채우기
    movable_rect.draw(screen)  # 움직이는 사각형 그리기
    fixed_rect.draw(screen)  # 고정된 사각형 그리기

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(60)

# 게임 종료
pygame.quit()