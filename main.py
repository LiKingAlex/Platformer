import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer with Menu")

# Load images
background = pygame.image.load("images/background.png")
player_img = pygame.image.load("images/Mario.png")
platform_img = pygame.image.load("images/platform.png")
food_img = pygame.image.load("images/food.png")
coin_img = pygame.image.load("images/coin.png")
enemy_img = pygame.image.load("images/enemy.png")
spike_img = pygame.image.load("images/spike.png")  # New spike image

bowser_img = pygame.image.load("images/Bowser.png")
fireball_img = pygame.image.load("images/fireball.png")


# Load sounds
jump_sfx = pygame.mixer.Sound("sounds/jump.mp3")
coin_sfx = pygame.mixer.Sound("sounds/coin.mp3")
hit_sfx = pygame.mixer.Sound("sounds/hit.mp3")
win_sfx = pygame.mixer.Sound("sounds/win.mp3")

# Background music (looped)
pygame.mixer.music.load("sounds/background.mp3")
music_on = True
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

levels = [
    # Level 1 (Intro – simple)
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(200, 450, 200, 20),
            pygame.Rect(500, 350, 200, 20),
        ],
        "food": pygame.Rect(600, 300, 50, 50),
        "coins": [pygame.Rect(250, 410, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(200, 420, 40, 40), "dir": 1, "speed": 1, "range": (200, 400)}
        ]
    },

    # Level 2
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 400, 200, 20),
            pygame.Rect(400, 300, 200, 20),
            pygame.Rect(600, 200, 150, 20),
        ],
        "food": pygame.Rect(650, 150, 50, 50),
        "coins": [pygame.Rect(150, 360, 30, 30), pygame.Rect(450, 260, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(400, 270, 40, 40), "dir": -1, "speed": 2, "range": (400, 600)}
        ]
    },

    # Level 3
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(150, 450, 150, 20),
            pygame.Rect(350, 350, 150, 20),
            pygame.Rect(550, 250, 150, 20),
            pygame.Rect(300, 150, 150, 20),
        ],
        "food": pygame.Rect(600, 100, 50, 50),
        "coins": [pygame.Rect(180, 410, 30, 30), pygame.Rect(370, 310, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(150, 420, 40, 40), "dir": 1, "speed": 2, "range": (150, 300)},
            {"rect": pygame.Rect(550, 220, 40, 40), "dir": -1, "speed": 2, "range": (550, 700)}
        ]
    },

    # Level 4 (add more enemies)
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 470, 200, 20),
            pygame.Rect(400, 380, 200, 20),
            pygame.Rect(200, 250, 200, 20),
            pygame.Rect(500, 150, 180, 20),
        ],
        "food": pygame.Rect(550, 100, 50, 50),
        "coins": [pygame.Rect(150, 430, 30, 30), pygame.Rect(450, 340, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(100, 440, 40, 40), "dir": -1, "speed": 3, "range": (100, 300)},
            {"rect": pygame.Rect(400, 350, 40, 40), "dir": 1, "speed": 2, "range": (400, 600)}
        ]
    },

    # Level 5: Spikes + more platform variety
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(120, 450, 180, 20),
            pygame.Rect(400, 350, 180, 20),
            pygame.Rect(620, 200, 160, 20),
            pygame.Rect(400, 100, 120, 20),
        ],
        "spikes": [pygame.Rect(300, 530, 50, 20), pygame.Rect(480, 330, 40, 20)],
        "food": pygame.Rect(650, 150, 50, 50),
        "coins": [pygame.Rect(150, 410, 30, 30), pygame.Rect(430, 310, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(120, 420, 40, 40), "dir": 1, "speed": 3, "range": (120, 300)},
            {"rect": pygame.Rect(400, 320, 40, 40), "dir": -1, "speed": 2, "range": (400, 580)}
        ]
    },

    # Level 6: Introduce moving platform + higher food
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 400, 200, 20),
            pygame.Rect(500, 300, 200, 20),
            pygame.Rect(300, 150, 200, 20),
        ],
        "moving_platforms": [
            {"rect": pygame.Rect(300, 220, 100, 20), "dir": 1, "axis": "x", "speed": 2, "range": (250, 450)}
        ],
        "spikes": [pygame.Rect(400, 530, 50, 20), pygame.Rect(120, 380, 40, 20)],
        "food": pygame.Rect(320, 100, 50, 50),
        "coins": [pygame.Rect(130, 360, 30, 30), pygame.Rect(530, 260, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(100, 370, 40, 40), "dir": -1, "speed": 2, "range": (100, 300)},
            {"rect": pygame.Rect(500, 270, 40, 40), "dir": 1, "speed": 2, "range": (500, 700)}
        ]
    },

    # Level 7: Tricky spike layout + fast enemy
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(600, 480, 180, 20),
            pygame.Rect(300, 360, 180, 20),
            pygame.Rect(100, 220, 180, 20),
        ],
        "moving_platforms": [
            {"rect": pygame.Rect(200, 300, 100, 20), "dir": -1, "axis": "x", "speed": 3, "range": (150, 400)}
        ],
        "spikes": [pygame.Rect(240, 530, 50, 20), pygame.Rect(620, 460, 50, 20)],
        "food": pygame.Rect(120, 170, 50, 50),
        "coins": [pygame.Rect(630, 440, 30, 30), pygame.Rect(330, 320, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(600, 450, 40, 40), "dir": 1, "speed": 4, "range": (600, 780)},
            {"rect": pygame.Rect(300, 330, 40, 40), "dir": -1, "speed": 2, "range": (300, 450)}
        ]
    },

    # Level 8: Vertical moving platform + multiple enemies
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(200, 460, 200, 20),
            pygame.Rect(400, 340, 200, 20),
            pygame.Rect(100, 220, 200, 20),
        ],
        "moving_platforms": [
            {"rect": pygame.Rect(500, 300, 100, 20), "dir": 1, "axis": "y", "speed": 2, "range": (280, 400)}
        ],
        "spikes": [pygame.Rect(220, 530, 60, 20), pygame.Rect(580, 530, 60, 20)],
        "food": pygame.Rect(130, 170, 50, 50),
        "coins": [pygame.Rect(230, 420, 30, 30), pygame.Rect(430, 300, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(200, 430, 40, 40), "dir": -1, "speed": 2, "range": (200, 400)},
            {"rect": pygame.Rect(400, 310, 40, 40), "dir": 1, "speed": 3, "range": (400, 600)}
        ]
    },

    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(200, 500, 200, 20),
            pygame.Rect(400, 320, 200, 20),
            pygame.Rect(100, 280, 200, 20),
        ],
        "moving_platforms": [
            {"rect": pygame.Rect(400, 300, 100, 20), "dir": 1, "axis": "y", "speed": 2, "range": (280, 400)}
        ],
        "spikes": [pygame.Rect(200, 530, 60, 20), pygame.Rect(580, 530, 60, 20)],
        "food": pygame.Rect(100, 170, 50, 50),
        "coins": [pygame.Rect(200, 420, 30, 30), pygame.Rect(430, 300, 30, 30)],
        "enemies": [
            {"rect": pygame.Rect(250, 430, 40, 40), "dir": -1, "speed": 2, "range": (200, 400)},
            {"rect": pygame.Rect(400, 310, 40, 40), "dir": 1, "speed": 3, "range": (400, 600)}
        ]
    },

    # Level 10
{
    "platforms": [
        pygame.Rect(0, 550, 800, 50),
        pygame.Rect(200, 500, 200, 20),
        pygame.Rect(400, 320, 200, 20),
        pygame.Rect(100, 280, 200, 20),
        pygame.Rect(600, 240, 150, 20),
        pygame.Rect(50, 180, 100, 20)
    ],
    "moving_platforms": [
        {"rect": pygame.Rect(300, 400, 100, 20), "dir": 1, "axis": "x", "speed": 2, "range": (200, 500)},
        {"rect": pygame.Rect(400, 300, 100, 20), "dir": 1, "axis": "y", "speed": 2, "range": (280, 400)}
    ],
    "spikes": [
        pygame.Rect(200, 530, 60, 20),
        pygame.Rect(580, 530, 60, 20),
        pygame.Rect(100, 530, 40, 20),
        pygame.Rect(700, 530, 60, 20)
    ],
    "food": pygame.Rect(100, 140, 50, 50),
    "coins": [
        pygame.Rect(220, 420, 30, 30),
        pygame.Rect(430, 300, 30, 30),
        pygame.Rect(650, 210, 30, 30),
        pygame.Rect(80, 150, 30, 30)
    ],
    "enemies": [
        {"rect": pygame.Rect(250, 430, 40, 40), "dir": -1, "speed": 2, "range": (200, 400)},
        {"rect": pygame.Rect(400, 310, 40, 40), "dir": 1, "speed": 3, "range": (400, 600)},
        {"rect": pygame.Rect(620, 210, 40, 40), "dir": -1, "speed": 2, "range": (600, 750)}
    ],
    "bowser": {
        "rect": pygame.Rect(680, 160, 60, 80),
        "cooldown": 90
    }
}

]


def draw_text_center(text, font, color, y):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (WIDTH//2 - rendered.get_width()//2, y))

def main_menu():
    menu_items = ["Start Game", "Load Level", "Settings", "Quit"]
    selected = 0

    while True:
        screen.fill((30, 30, 30))
        draw_text_center("Main Menu", font, (255, 255, 255), 100)

        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            draw_text_center(item, small_font, color, 200 + i * 50)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if menu_items[selected] == "Start Game":
                        run_game(0)
                    elif menu_items[selected] == "Load Level":
                        chosen = load_level_menu()
                        if chosen is not None:
                            run_game(chosen)
                    elif menu_items[selected] == "Settings":
                        settings_menu()
                    elif menu_items[selected] == "Quit":
                        pygame.quit()
                        sys.exit()

def load_level_menu():
    selected = 0
    levels_per_column = 5
    column_spacing = 200
    top_margin = 200

    while True:
        screen.fill((30, 30, 30))
        draw_text_center("Select Level", font, (255, 255, 255), 100)

        for i in range(len(levels)):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            
            # Column and row position
            col = i // levels_per_column
            row = i % levels_per_column

            x = WIDTH // 2 - column_spacing // 2 + col * column_spacing
            y = top_margin + row * 50

            text = small_font.render(f"Level {i + 1}", True, color)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

        draw_text_center("Press ESC to return", small_font, (200, 200, 200), HEIGHT - 50)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                elif event.key == pygame.K_LEFT:
                    if selected >= levels_per_column:
                        selected -= levels_per_column
                elif event.key == pygame.K_RIGHT:
                    if selected + levels_per_column < len(levels):
                        selected += levels_per_column
                elif event.key == pygame.K_RETURN:
                    return selected
                elif event.key == pygame.K_ESCAPE:
                    return None

def settings_menu():
    global music_on
    volume = pygame.mixer.music.get_volume()
    selected = 0
    options = ["Volume", "Toggle Music", "Back"]

    while True:
        screen.fill((30, 30, 30))
        draw_text_center("Settings", font, (255, 255, 255), 100)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            if option == "Volume":
                text = f"Volume: {int(volume * 100)}%"
            elif option == "Toggle Music":
                text = "Music: ON" if music_on else "Music: OFF"
            else:
                text = option

            draw_text_center(text, small_font, color, 200 + i * 50)

        draw_text_center("Use LEFT/RIGHT to change", small_font, (200, 200, 200), HEIGHT - 80)
        draw_text_center("Press ESC to return", small_font, (200, 200, 200), HEIGHT - 50)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_LEFT:
                    if options[selected] == "Volume":
                        volume = max(0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_RIGHT:
                    if options[selected] == "Volume":
                        volume = min(1, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Toggle Music":
                        if music_on:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        music_on = not music_on

def run_game(start_level=0):
    player = pygame.Rect(100, 500, 50, 50)
    player_speed = 10
    jump_power = 25
    gravity = 1

    vel_y = 0
    on_ground = False
    can_double_jump = False
    double_jump_used = False

    current_level = start_level
    score = 0
    lives = 3
    paused = False
    win = False
    game_over = False

    platforms = []
    food = None
    coins = []
    enemies = []
    door = None
    

    def load_level(index):
        nonlocal platforms, food, coins, enemies, door
        nonlocal vel_y, on_ground, can_double_jump, double_jump_used
        nonlocal player
        

        level = levels[index]
        platforms = level["platforms"]
        food = level["food"].copy() if hasattr(level["food"], 'copy') else level["food"]  # Make sure it's a new Rect
        coins = [coin.copy() for coin in level["coins"]]
        enemies = []
        for enemy in level["enemies"]:
            # Create a new dict with a new rect object
            enemies.append({
                "rect": enemy["rect"].copy(),
                "dir": enemy["dir"],
                "speed": enemy["speed"],
                "range": enemy["range"]
            })
        door = pygame.Rect(platforms[-1].x + 80, platforms[-1].y - 60, 40, 60)
        player.topleft = (100, 500)

        vel_y = 0
        on_ground = False
        can_double_jump = False
        double_jump_used = False


    load_level(current_level)

    def draw():
        screen.blit(background, (0, 0))

        if game_over or win:
            msg = "You Win!" if win else "Game Over"
            end_text = font.render(msg, True, (0, 255, 0) if win else (255, 0, 0))
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 80))

            retry_text = small_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
            screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))

            pygame.display.flip()
            return

        for plat in platforms:
            tile_width = platform_img.get_width()
            x = plat.left
            while x < plat.right:
                screen.blit(platform_img, (x, plat.top))
                x += tile_width

        screen.blit(food_img, food.topleft)
        for coin in coins:
            screen.blit(coin_img, coin.topleft)
        for enemy in enemies:
            screen.blit(enemy_img, enemy["rect"].topleft)

       

        pygame.draw.rect(screen, (0, 255, 0), door)
        screen.blit(player_img, player.topleft)

        level_text = small_font.render(f"Level: {current_level + 1}", True, (255, 255, 255))
        score_text = small_font.render(f"Score: {score}", True, (255, 255, 0))
        lives_text = small_font.render(f"Lives: {lives}", True, (255, 100, 100))
        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(lives_text, (10, 70))

        if paused:
            pause_text = font.render("Paused", True, (255, 255, 255))
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    def move_player(keys):
        nonlocal vel_y, on_ground, can_double_jump, double_jump_used
        nonlocal current_level, score, lives, paused, game_over, win
        nonlocal player

        if paused or win or game_over:
            return

        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_SPACE]:
            if on_ground:
                vel_y = -jump_power
                jump_sfx.play()
                on_ground = False
                double_jump_used = False
            elif can_double_jump and not double_jump_used:
                vel_y = -jump_power
                jump_sfx.play()
                double_jump_used = True

        player.left = max(0, player.left)
        player.right = min(WIDTH, player.right)

        vel_y += gravity
        player.y += vel_y

        on_ground = False
        for plat in platforms:
            if player.colliderect(plat):
                if vel_y > 0 and player.bottom - vel_y <= plat.top:
                    player.bottom = plat.top
                    vel_y = 0
                    on_ground = True
                elif vel_y < 0 and player.top - vel_y >= plat.bottom:
                    player.top = plat.bottom
                    vel_y = 0

        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
            vel_y = 0
            on_ground = True

        if player.colliderect(food):
            can_double_jump = True
            food.x = -100

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 10
                coin_sfx.play()

        for enemy in enemies:
            enemy_rect = enemy["rect"]
            enemy_rect.x += enemy["dir"] * enemy["speed"]
            if enemy_rect.left < enemy["range"][0] or enemy_rect.right > enemy["range"][1]:
                enemy["dir"] *= -1
            if player.colliderect(enemy_rect):
                lives -= 1
                hit_sfx.play()
                if lives <= 0:
                    game_over = True
                else:
                    player.topleft = (100, 500)
                    vel_y = 0
                    on_ground = False
                    can_double_jump = False
                    double_jump_used = False

        if player.colliderect(door):
            current_level += 1
            if current_level >= len(levels):
                win = True
                win_sfx.play()
            else:
                load_level(current_level)

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not (game_over or win):
                    paused = not paused
                if (game_over or win) and event.key == pygame.K_r:
                    # Restart
                    current_level = 0
                    score = 0
                    lives = 3
                    win = False
                    game_over = False
                    load_level(current_level)
                if (game_over or win) and event.key == pygame.K_q:
                    return  # Return to main menu

        move_player(keys)
        draw()

def main():
    while True:
        main_menu()

if __name__ == "__main__":
    main()
