import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 원의 초기 위치 및 속도 설정
circle_x = 400
circle_y = 300
speed = 9

clock = pygame.time.Clock()
running = True

# 메인 루프
while running:
    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. 키 입력 확인 (연속 입력 처리에 적합)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle_x -= speed
    if keys[pygame.K_RIGHT]:
        circle_x += speed
    if keys[pygame.K_UP]:
        circle_y -= speed
    if keys[pygame.K_DOWN]:
        circle_y += speed
            
    # 3. 화면 그리기
    screen.fill(WHITE)
    # 고정된 숫자 대신 변수 circle_x, circle_y를 사용합니다.
    pygame.draw.circle(screen, BLUE, (circle_x, circle_y), 50)
    
    # 4. 화면 업데이트
    pygame.display.flip()
    
    # 5. 프레임 제한 (초당 60프레임)
    clock.tick(60)

# 종료
pygame.quit()
sys.exit()
