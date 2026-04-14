import pygame
import sys
import math

# 1. 초기화 및 창 설정
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("3가지 충돌 방식 시각화 (AABB, OBB, Circle)")

# 폰트 설정
font = pygame.font.SysFont("Arial", 24, bold=True)

# 색상 정의
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BG_COLOR = (30, 30, 30)

# 오브젝트 설정
static_orig_width, static_orig_height = 100, 100
static_center_pos = (screen_width // 2, screen_height // 2)
static_angle = 0
base_rotation_speed = 1.0
boost_rotation_speed = 5.0

moving_rect = pygame.Rect(100, 100, 80, 80)
move_speed = 5

def get_obb_vertices(center, width, height, angle):
    """중심, 크기, 각도를 입력받아 OBB의 네 꼭짓점 좌표를 반환"""
    angle_rad = math.radians(-angle)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    hw, hh = width / 2, height / 2
    pts = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    rotated_pts = []
    for x, y in pts:
        rx = x * cos_a - y * sin_a + center[0]
        ry = x * sin_a + y * cos_a + center[1]
        rotated_pts.append(pygame.Vector2(rx, ry))
    return rotated_pts

def check_obb_collision(poly1, poly2):
    """분리축 이론(SAT)을 이용한 두 볼록 다각형 충돌 감지"""
    polygons = [poly1, poly2]
    for i in range(2):
        poly = polygons[i]
        for j in range(len(poly)):
            # 변의 수직 벡터(법선) 구하기
            p1 = poly[j]
            p2 = poly[(j + 1) % len(poly)]
            edge = p2 - p1
            axis = pygame.Vector2(-edge.y, edge.x).normalize()
            
            # 두 다각형을 축에 투영
            min1 = max1 = poly1[0].dot(axis)
            for p in poly1[1:]:
                proj = p.dot(axis)
                min1, max1 = min(min1, proj), max(max1, proj)
                
            min2 = max2 = poly2[0].dot(axis)
            for p in poly2[1:]:
                proj = p.dot(axis)
                min2, max2 = min(min2, proj), max(max2, proj)
            
            # 겹치지 않는 구간이 하나라도 있으면 충돌 아님
            if max1 < min2 or max2 < min1:
                return False
    return True

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: moving_rect.x -= move_speed
    if keys[pygame.K_RIGHT]: moving_rect.x += move_speed
    if keys[pygame.K_UP]: moving_rect.y -= move_speed
    if keys[pygame.K_DOWN]: moving_rect.y += move_speed

    # 회전 처리
    rot_speed = boost_rotation_speed if keys[pygame.K_z] else base_rotation_speed
    static_angle = (static_angle + rot_speed) % 360

    # 1. 시각용 Surface 생성
    static_surf = pygame.Surface((static_orig_width, static_orig_height), pygame.SRCALPHA)
    static_surf.fill(GRAY)
    rotated_surf = pygame.transform.rotate(static_surf, static_angle)
    rotated_rect = rotated_surf.get_rect(center=static_center_pos)

    # --- 충돌 감지 ---
    # AABB 충돌 (빨간 박스 기준)
    aabb_hit = rotated_rect.colliderect(moving_rect)

    # 원형 충돌 (파란 원 기준)
    static_radius = static_orig_width // 2
    moving_radius = moving_rect.width // 2
    dist = pygame.Vector2(static_center_pos).distance_to(moving_rect.center)
    circle_hit = dist <= (static_radius + moving_radius)

    # OBB 충돌 (초록 박스 기준)
    poly_static = get_obb_vertices(static_center_pos, static_orig_width, static_orig_height, static_angle)
    # 이동 사각형은 회전이 0도인 OBB로 간주
    poly_moving = get_obb_vertices(moving_rect.center, moving_rect.width, moving_rect.height, 0)
    obb_hit = check_obb_collision(poly_static, poly_moving)

    # --- 그리기 작업 ---
    screen.fill(BG_COLOR)

    # 오브젝트 본체
    screen.blit(rotated_surf, rotated_rect)
    pygame.draw.rect(screen, GRAY, moving_rect)

    # 바운딩 박스 시각화
    pygame.draw.rect(screen, RED, rotated_rect, 2)  # AABB
    pygame.draw.rect(screen, RED, moving_rect, 2)
    pygame.draw.circle(screen, BLUE, static_center_pos, static_radius, 2) # Circle
    pygame.draw.circle(screen, BLUE, moving_rect.center, moving_radius, 2)
    pygame.draw.polygon(screen, GREEN, poly_static, 2) # OBB
    pygame.draw.polygon(screen, GREEN, poly_moving, 2)

    # 결과 UI 표시 (왼쪽 상단)
    texts = [
        (f"Circle: {'HIT' if circle_hit else 'IDLE'}", BLUE),
        (f"AABB: {'HIT' if aabb_hit else 'IDLE'}", RED),
        (f"OBB: {'HIT' if obb_hit else 'IDLE'}", GREEN)
    ]

    for i, (msg, color) in enumerate(texts):
        img = font.render(msg, True, color)
        screen.blit(img, (20, 20 + (i * 30)))

    pygame.display.flip()
    clock.tick(60)
