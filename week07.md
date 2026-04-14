import pygame, sys, random

# 1. 초기화
pygame.init()
W, H = 800, 400
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
f = pygame.font.SysFont(None, 30)

def reset():
    global p, hp, sc, st, en, tm, sk
    p = pygame.Rect(400, 200, 30, 40)
    # 요청하신 대로 HP를 3으로 수정했습니다!
    hp, sc, st, en, tm, sk = 3, 0, "GO", [], 0, 0

reset()

# 2. 메인 루프
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
            if st != "GO": reset()

    if st == "GO":
        k = pygame.key.get_pressed()
        if k[pygame.K_LEFT] and p.x > 0: p.x -= 6
        if k[pygame.K_RIGHT] and p.x < W-30: p.x += 6
        if k[pygame.K_UP] and p.y > 0: p.y -= 6
        if k[pygame.K_DOWN] and p.y < H-40: p.y += 6

        tm += 1
        if tm > 15: # 미사일 생성 간격을 조금 더 좁혔습니다
            x = -50 if random.random() > 0.5 else W+50
            v = random.uniform(7, 13) if x < 0 else random.uniform(-13, -7)
            ry = random.randint(0, H-12)
            en.append({"r": pygame.Rect(x, ry, 45, 12), "v": v})
            tm = 0

        for e in en[:]:
            e["r"].x += e["v"]
            if p.colliderect(e["r"]):
                en.remove(e); hp -= 1; sk = 20 # 피격 흔들림 강화
                if hp <= 0: st = "DIE"
                continue
            
            # 화면 밖 (점수 획득)
            if e["r"].x < -100 or e["r"].x > W+100:
                en.remove(e); sc += 20
                if sc >= 1000: st = "WIN"

    # 3. 그리기
    screen.fill((20, 20, 35))
    ox = random.randint(-sk, sk) if sk > 0 else 0
    oy = random.randint(-sk, sk) if sk > 0 else 0
    if sk > 0: sk -= 1

    for e in en:
        pygame.draw.rect(screen, (255, 60, 60), (e["r"].x+ox, e["r"].y+oy, 45, 12))
    pygame.draw.rect(screen, (0, 255, 255), (p.x+ox, p.y+oy, 30, 40))

    # UI (HP 상태 강조)
    hp_color = (255, 255, 255) if hp > 1 else (255, 0, 0)
    info = f.render(f"HP: {hp}  SCORE: {sc}/1000", True, hp_color)
    screen.blit(info, (20, 20))

    if st != "GO":
        msg = "LEGENDARY!" if st == "WIN" else "GAME OVER"
        screen.blit(f.render(msg, True, (255,255,0)), (330, 180))
        screen.blit(f.render("Press R to Restart", True, (255,255,255)), (320, 220))

    pygame.display.flip()
    clock.tick(60)
