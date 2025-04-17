import random
import math
from hero import Hero
from zombie_enemy import ZombieEnemy
from flying_enemy import FlyingEnemy

WIDTH = 1200
HEIGHT = 720

CHAR_SIZE = 120
CHAR_HALF = CHAR_SIZE / 2

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
SETTINGS = "settings"
game_state = MENU

score = 0
sound_on = True
sound_volume = 0.1

BG_COUNT = 10
BG_FRAMES = [f"bg{i}" for i in range(BG_COUNT)]
bg_index = 0.0
music_playing = False
enemy_spawn_timer = 0
enemies = []

hero = Hero((100, HEIGHT - CHAR_HALF))

BONUS_SIZE = 40
bonus_x = random.randint(int(CHAR_HALF), WIDTH - int(CHAR_HALF))
bonus_y = 0
bonus_speed = 3


def draw():
    screen.clear()

    if game_state == MENU:
        draw_button(WIDTH//2 - 100, HEIGHT//2 - 80, "Oyuna Başla")
        draw_button(WIDTH//2 - 100, HEIGHT//2 - 10, "Ayarlar")
        draw_button(WIDTH//2 - 100, HEIGHT//2 + 60, "Çıkış")

    elif game_state == SETTINGS:
        screen.draw.text("Ayarlar Menüsü", center=(WIDTH//2, HEIGHT//2 - 150), fontsize=50, color="white")
        draw_button(WIDTH//2 - 100, HEIGHT//2 - 40, "Sesi " + ("Kapat" if sound_on else "Aç"))
        draw_button(WIDTH//2 - 100, HEIGHT//2 + 30, f"Ses: %{int(sound_volume * 100)}")
        draw_button(WIDTH//2 - 100, HEIGHT//2 + 100, "Geri Dön")

    elif game_state == PLAYING:
        idx = int(bg_index) % BG_COUNT
        screen.blit(BG_FRAMES[idx], (0, 0))
        screen.draw.filled_rect(Rect((0, HEIGHT - 20), (WIDTH, 20)), 'green')
        screen.draw.text(f"Puan: {score}", topleft=(10, 10), fontsize=40, color='white')
        hero.draw()
        for e in enemies:
            e.draw()
        br = Rect((bonus_x - BONUS_SIZE / 2, bonus_y - BONUS_SIZE / 2), (BONUS_SIZE, BONUS_SIZE))
        screen.draw.filled_rect(br, 'yellow')

    elif game_state == GAME_OVER:
        screen.draw.text("Oyun Bitti", center=(WIDTH//2, HEIGHT//2 - 30), fontsize=60, color='red')
        draw_button(WIDTH//2 - 100, HEIGHT//2 + 10, "Tekrar Başla")
        draw_button(WIDTH//2 - 100, HEIGHT//2 + 70, "Menüye Dön")


def draw_button(x, y, text):
    rect = Rect((x, y), (200, 50))
    screen.draw.filled_rect(rect, 'darkgrey')
    screen.draw.text(text, center=rect.center, fontsize=36, color='white')


def update():
    global game_state, score, bonus_x, bonus_y, bg_index, enemy_spawn_timer, music_playing

    if game_state == PLAYING:
        bg_index = (bg_index + 0.15) % BG_COUNT
        hero.update(sound_on, sound_volume)
        enemy_spawn_timer += 1

        if enemy_spawn_timer > 50:
            if random.random() < 0.7:
                enemies.append(ZombieEnemy((WIDTH + 50, HEIGHT - CHAR_HALF)))
            else:
                fly_height = random.randint(150, 400)
                enemies.append(FlyingEnemy((WIDTH + 50, fly_height)))
            enemy_spawn_timer = 0

        for e in enemies[:]:
            e.update()
            if e.x < -CHAR_HALF:
                enemies.remove(e)
                continue

            if hero.colliderect(e):
                hdist = abs(hero.x - e.x)
                vdist = abs(hero.y - e.y)
                if hero.vy > 0 and hero.bottom <= e.top + 10 and hdist < CHAR_HALF:
                    score += 1
                    hero.vy = -14
                    hero.on_ground = False
                    enemies.remove(e)
                    if sound_on:
                        sounds.enemy_hit.set_volume(sound_volume)
                        sounds.enemy_hit.play()
                elif hdist < CHAR_HALF * 0.7 and vdist < CHAR_HALF * 0.7:
                    game_state = GAME_OVER
                    if music_playing:
                        sounds.bg_music.stop()
                        music_playing = False

        bonus_y += bonus_speed
        if bonus_y > HEIGHT:
            bonus_y = 0
            bonus_x = random.randint(int(CHAR_HALF), WIDTH - int(CHAR_HALF))

        br = Rect((bonus_x - BONUS_SIZE // 2, bonus_y - BONUS_SIZE // 2), (BONUS_SIZE, BONUS_SIZE))
        if hero.colliderect(br):
            score += 5
            bonus_y = 0
            bonus_x = random.randint(int(CHAR_HALF), WIDTH - int(CHAR_HALF))
            if sound_on:
                sounds.bonus.set_volume(sound_volume)
                sounds.bonus.play()

    if game_state == PLAYING:
        if sound_on and not music_playing:
            sounds.bg_music.set_volume(sound_volume)
            sounds.bg_music.play(-1)
            music_playing = True
        elif not sound_on and music_playing:
            sounds.bg_music.stop()
            music_playing = False


def on_key_down(key):
    global game_state, sound_on, sound_volume

    if key == keys.ESCAPE:
        if game_state == PLAYING:
            game_state = SETTINGS
        elif game_state == SETTINGS:
            game_state = PLAYING

    elif game_state == SETTINGS:
        if key == keys.K_1:
            sound_on = not sound_on
        elif key == keys.K_2:
            sound_volume = max(0.0, min(1.0, sound_volume + 0.1))

    elif game_state == PLAYING:
        if key == keys.SPACE:
            hero.jump(sound_on, sound_volume)
        elif key == keys.LEFT:
            hero.vx = -4
        elif key == keys.RIGHT:
            hero.vx = 4


def on_key_up(key):
    if game_state == PLAYING and key in (keys.LEFT, keys.RIGHT):
        hero.vx = 0


def on_mouse_down(pos):
    global game_state, score, bonus_x, bonus_y, enemies
    x, y = pos

    def in_box(x1, y1):
        return x1 < x < x1+200 and y1 < y < y1+50

    if game_state == MENU:
        if in_box(WIDTH//2 - 100, HEIGHT//2 - 80):
            game_state = PLAYING
            reset_game()
        elif in_box(WIDTH//2 - 100, HEIGHT//2 - 10):
            game_state = SETTINGS
        elif in_box(WIDTH//2 - 100, HEIGHT//2 + 60):
            exit()

    elif game_state == GAME_OVER:
        if in_box(WIDTH//2 - 100, HEIGHT//2 + 10):
            game_state = PLAYING
            reset_game()
        elif in_box(WIDTH//2 - 100, HEIGHT//2 + 70):
            game_state = MENU

    elif game_state == SETTINGS:
        if in_box(WIDTH//2 - 100, HEIGHT//2 - 40):
            global sound_on
            sound_on = not sound_on
        elif in_box(WIDTH//2 - 100, HEIGHT//2 + 30):
            global sound_volume
            sound_volume = (sound_volume + 0.1) % 1.1
        elif in_box(WIDTH//2 - 100, HEIGHT//2 + 100):
            game_state = PLAYING


def reset_game():
    global score, bonus_x, bonus_y, enemies
    score = 0
    bonus_y = 0
    bonus_x = random.randint(int(CHAR_HALF), WIDTH - int(CHAR_HALF))
    enemies.clear()
    hero.pos = (100, HEIGHT - CHAR_HALF)
    hero.vx = 0
    hero.vy = 0
    hero.on_ground = True


if __name__ == '__main__':
    import pgzrun
    pgzrun.go()
