import pygame
import math

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('AABB and OBB Collision Example')

# 색상 정의
GRAY = (169, 169, 169)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# 사각형 클래스 정의
class Rectangle:
    def __init__(self, x, y, width, height, movable=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movable = movable  # 움직일 수 있는지 여부
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.angle = 0  # 회전 각도
        self.rotation_speed = 1  # 회전 속도 (기본값은 1)

    def draw(self, screen):
        # 회색 사각형 그리기
        pygame.draw.rect(screen, GRAY, self.rect)
        # 빨간색 AABB (테두리) 그리기
        pygame.draw.rect(screen, RED, self.rect, 2)

    def move(self, dx, dy):
        if self.movable:
            self.rect.x += dx
            self.rect.y += dy

    def get_center(self):
        # 사각형의 중심 좌표 반환
        return self.rect.center

    def get_radius(self):
        # 원의 반지름은 너비의 절반
        return self.width // 2

    def draw_circle(self, screen):
        # 중심에서 파란 원 그리기
        center = self.get_center()
        radius = self.get_radius()
        pygame.draw.circle(screen, BLUE, center, radius, 2)  # 파란 원

    def check_collision(self, other):
        # 두 원의 충돌 감지 (두 원의 거리 < 두 원의 반지름 합이면 충돌)
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        return distance < (self.get_radius() + other.get_radius())

    def rotate(self):
        # 회전
        self.angle += self.rotation_speed
        if self.angle >= 360:
            self.angle -= 360

    def draw_rotated(self, screen):
        # 회전된 사각형을 그리는 함수
        # 사각형의 중심을 기준으로 회전시킨 후 그리기
        rotated_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rotated_image.fill((0, 0, 0, 0))  # 투명 배경으로 설정
        pygame.draw.rect(rotated_image, GRAY, (0, 0, self.width, self.height))
        rotated_image = pygame.transform.rotate(rotated_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect.topleft)

        # OBB (회전된 경계 상자) 그리기
        pygame.draw.rect(screen, GREEN, rotated_rect, 2)

    def get_axes(self, other):
        # 각 사각형에서 2개의 축을 얻습니다. 사각형의 두 변에서 법선 벡터를 계산합니다.
        axes = []
        for rect in [self, other]:
            corners = [pygame.math.Vector2(rect.rect.topleft), pygame.math.Vector2(rect.rect.topright),
                       pygame.math.Vector2(rect.rect.bottomright), pygame.math.Vector2(rect.rect.bottomleft)]
            for i in range(4):
                p1 = corners[i]
                p2 = corners[(i + 1) % 4]
                edge = p2 - p1
                axis = pygame.math.Vector2(-edge.y, edge.x)  # 법선 벡터
                axes.append(axis.normalize())  # 정규화된 축 추가
        return axes

    def project(self, axis):
        # 사각형을 주어진 축으로 투영하여 최소값과 최대값을 반환합니다.
        corners = [pygame.math.Vector2(self.rect.topleft), pygame.math.Vector2(self.rect.topright),
                   pygame.math.Vector2(self.rect.bottomright), pygame.math.Vector2(self.rect.bottomleft)]
        projections = [corner.dot(axis) for corner in corners]
        return min(projections), max(projections)

    def project_onto_axis(self, axis, other):
        # 각 사각형을 주어진 축(axis)으로 투영하여, 교차하는지 확인
        projection1 = self.project(axis)
        projection2 = other.project(axis)
        return not (projection1[1] < projection2[0] or projection2[1] < projection1[0])

    def check_obb_collision(self, other):
        # OBB 충돌 감지: SAT (분리축 정리) 적용
        axes = self.get_axes(other)
        for axis in axes:
            if not self.project_onto_axis(axis, other):
                return False  # 한 축이라도 겹치지 않으면 충돌 아님
        return True  # 모든 축에서 겹치면 충돌


# 오브젝트 생성
movable_rect = Rectangle(100, 100, 50, 50, movable=True)  # 움직일 수 있는 사각형
fixed_rect = Rectangle(375, 275, 50, 50)  # 화면 중앙에 고정된 사각형

# 게임 루프
running = True
clock = pygame.time.Clock()
background_color = (0, 0, 0)  # 기본 배경 색 (검정)

# 충돌 상태 표시 변수
circle_hit = False
aabb_hit = False
obb_hit = False

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

    # Z 키를 눌러 회전 속도 증가
    if keys[pygame.K_z]:
        fixed_rect.rotation_speed = 5  # 회전 속도 빠르게

    # 움직일 수 있는 사각형 이동
    movable_rect.move(dx, dy)

    # 충돌 감지 (각각)
    circle_hit = movable_rect.check_collision(fixed_rect)  # 원형 충돌 감지
    aabb_hit = movable_rect.rect.colliderect(fixed_rect.rect)  # AABB 충돌 감지
    obb_hit = movable_rect.check_obb_collision(fixed_rect)  # OBB 충돌 감지

    # 충돌 시 배경 색을 변경
    if circle_hit or aabb_hit or obb_hit:
        background_color = RED  # 충돌 시 배경 색을 빨간색으로 변경
    else:
        background_color = (0, 0, 0)  # 충돌 안 하면 배경 색을 검정으로 유지

    # 고정된 사각형 회전
    fixed_rect.rotate()

    # 화면에 그리기
    screen.fill(background_color)  # 배경 색 설정
    movable_rect.draw(screen)  # 움직이는 사각형 그리기
    movable_rect.draw_circle(screen)  # 움직이는 사각형의 원 그리기
    fixed_rect.draw_rotated(screen)  # 회전된 고정된 사각형 그리기

    # 충돌 결과 메시지 표시
    font = pygame.font.Font(None, 36)
    if circle_hit:
        circle_text = font.render("Circle: HIT", True, WHITE)
        screen.blit(circle_text, (10, 10))
    if aabb_hit:
        aabb_text = font.render("AABB: HIT", True, WHITE)
        screen.blit(aabb_text, (10, 50))
    if obb_hit:
        obb_text = font.render("OBB: HIT", True, WHITE)
        screen.blit(obb_text, (10, 90))

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(60)

# 게임 종료
pygame.quit()