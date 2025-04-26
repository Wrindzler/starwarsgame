import pygame
import sys
import os
from game_manager import GameManager
from location import Location
from good_characters import LukeSkywalker, MasterYoda
from bad_characters import DarthVader, KyloRen, Stormtrooper

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_RED = (139, 0, 0)

CELL_SIZE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Star Wars Labirent Oyunu")

font = pygame.font.SysFont('Arial', 20)
small_font = pygame.font.SysFont('Arial', 14)
large_font = pygame.font.SysFont('Arial', 30)

game_manager = GameManager("Star wars harita.txt")

def load_sound(filename):
    try:
        sound = pygame.mixer.Sound(filename)
        sound.set_volume(0.1)
        return sound
    except:
        print(f"Ses dosyası yüklenemedi: {filename}")
        return None

giris_sound = load_sound("giris.mp3")
yakalanma_sound = load_sound("yakalanma.mp3")

def load_image(name, size=(CELL_SIZE, CELL_SIZE)):
    try:
        image = pygame.image.load(f"gorseller/{name}.png")
        return pygame.transform.scale(image, size)
    except:
        surf = pygame.Surface(size)
        surf.fill(WHITE)
        pygame.draw.rect(surf, RED, (0, 0, size[0], size[1]), 2)
        return surf

try:
    luke_img = load_image("luke", (150, 150))
    yoda_img = load_image("yoda", (150, 150))
    
    luke_game_img = load_image("luke", (CELL_SIZE, CELL_SIZE))
    yoda_game_img = load_image("yoda", (CELL_SIZE, CELL_SIZE))
    vader_img = load_image("vader", (CELL_SIZE, CELL_SIZE))
    kylo_img = load_image("kylo", (CELL_SIZE, CELL_SIZE))
    trooper_img = load_image("trooper", (CELL_SIZE, CELL_SIZE))
    
    cup_img = load_image("kupa")
    heart_full_img = load_image("kalp", (30, 30))
    heart_half_img = load_image("yarım_kalp", (30, 30))
    heart_empty_img = load_image("bitmiş_kalp", (30, 30))
    
    arrow_up_img = load_image("yukarı_bakan_ok", (30, 30))
    arrow_down_img = load_image("aşağı_bakan_ok", (30, 30))
    arrow_left_img = load_image("sola_bakan_ok", (30, 30))
    arrow_right_img = load_image("sağa_bakan_ok", (30, 30))
except:
    luke_img = pygame.Surface((150, 150))
    luke_img.fill(BLUE)
    yoda_img = pygame.Surface((150, 150))
    yoda_img.fill(GREEN)
    luke_game_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    luke_game_img.fill(BLUE)
    yoda_game_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    yoda_game_img.fill(GREEN)
    vader_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    vader_img.fill(RED)
    kylo_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    kylo_img.fill((150, 0, 0))
    trooper_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    trooper_img.fill((200, 200, 200))
    cup_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    cup_img.fill(YELLOW)
    heart_full_img = pygame.Surface((30, 30))
    heart_full_img.fill(RED)
    heart_half_img = pygame.Surface((30, 30))
    heart_half_img.fill((255, 128, 0))
    heart_empty_img = pygame.Surface((30, 30))
    heart_empty_img.fill(GRAY)
    arrow_up_img = pygame.Surface((30, 30))
    arrow_up_img.fill(BLUE)
    arrow_down_img = pygame.Surface((30, 30))
    arrow_down_img.fill(BLUE)
    arrow_left_img = pygame.Surface((30, 30))
    arrow_left_img.fill(BLUE)
    arrow_right_img = pygame.Surface((30, 30))
    arrow_right_img.fill(BLUE)

def character_selection_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen
    selection = None
    
    if giris_sound:
        giris_sound.play(-1)
    
    while selection is None:
        screen.fill(BLACK)
        
        title = large_font.render("Karakter Seçimi", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        rules_title = font.render("Oyun Kuralları:", True, YELLOW)
        screen.blit(rules_title, (SCREEN_WIDTH // 2 - rules_title.get_width() // 2, 100))
        
        general_rules = [
            "• Yön tuşları ile karakterinizi hareket ettirin",
            "• Kötü karakterlerden kaçının",
            "• Kupa ile oyunu kazanın",
            "• R tuşu ile yeniden başlayın"
        ]
        
        for i, rule in enumerate(general_rules):
            rule_text = small_font.render(rule, True, WHITE)
            screen.blit(rule_text, (SCREEN_WIDTH // 2 - rule_text.get_width() // 2, 130 + i * 20))
        
        luke_rect = pygame.Rect(SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200)
        pygame.draw.rect(screen, BLUE, luke_rect, 2)
        screen.blit(luke_img, (luke_rect.centerx - luke_img.get_width() // 2, luke_rect.centery - luke_img.get_height() // 2))
        luke_text = font.render("Luke Skywalker", True, WHITE)
        screen.blit(luke_text, (luke_rect.centerx - luke_text.get_width() // 2, luke_rect.bottom + 10))
        
        luke_features = [
            "• 3 can hakkı",
            "• Her yakalanmada 1 can kaybı"
        ]
        
        for i, feature in enumerate(luke_features):
            feature_text = small_font.render(feature, True, WHITE)
            screen.blit(feature_text, (luke_rect.centerx - feature_text.get_width() // 2, luke_rect.bottom + 40 + i * 20))
        
        yoda_rect = pygame.Rect(3 * SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200)
        pygame.draw.rect(screen, GREEN, yoda_rect, 2)
        screen.blit(yoda_img, (yoda_rect.centerx - yoda_img.get_width() // 2, yoda_rect.centery - yoda_img.get_height() // 2))
        yoda_text = font.render("Master Yoda", True, WHITE)
        screen.blit(yoda_text, (yoda_rect.centerx - yoda_text.get_width() // 2, yoda_rect.bottom + 10))
        
        yoda_features = [
            "• 3 can hakkı",
            "• Her yakalanmada 0.5 can kaybı"
        ]
        
        for i, feature in enumerate(yoda_features):
            feature_text = small_font.render(feature, True, WHITE)
            screen.blit(feature_text, (yoda_rect.centerx - feature_text.get_width() // 2, yoda_rect.bottom + 40 + i * 20))
        
        select_text = font.render("Karakterinizi seçmek için üzerine tıklayın", True, YELLOW)
        screen.blit(select_text, (SCREEN_WIDTH // 2 - select_text.get_width() // 2, SCREEN_HEIGHT - 100))
        
        controls_text = small_font.render("Çıkış için pencereyi kapatın", True, GRAY)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                if not (screen.get_flags() & pygame.FULLSCREEN):
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if luke_rect.collidepoint(mouse_pos):
                    selection = "Luke"
                elif yoda_rect.collidepoint(mouse_pos):
                    selection = "Yoda"
    
    if giris_sound:
        giris_sound.stop()
    
    return selection

def draw_maze(maze, offset_x, offset_y, game_manager):
    panel_width = len(maze[0]) * CELL_SIZE + 80
    panel_height = len(maze) * CELL_SIZE + 80
    panel_rect = pygame.Rect(offset_x - 40, offset_y - 40, panel_width, panel_height)
    pygame.draw.rect(screen, LIGHT_BLUE, panel_rect)
    pygame.draw.rect(screen, BLACK, panel_rect, 2)
    
    path_info = game_manager.get_shortest_path_info()
    shortest_path_coords = set()
    
    if path_info:
        shortest = min(path_info, key=lambda x: x[1])
        path = shortest[2] if len(shortest) > 2 else []
        if path:
            shortest_path_coords = {(loc.get_x(), loc.get_y()) for loc in path}
    
    for i in range(len(maze[0])):
        num_text = small_font.render(str(i), True, BLACK)
        screen.blit(num_text, (offset_x + i * CELL_SIZE + CELL_SIZE//2 - num_text.get_width()//2, offset_y - 25))
    
    for i in range(len(maze)):
        num_text = small_font.render(str(i), True, BLACK)
        screen.blit(num_text, (offset_x - 25, offset_y + i * CELL_SIZE + CELL_SIZE//2 - num_text.get_height()//2))
    
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                if (x, y) in shortest_path_coords:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
            
            cell_text = small_font.render(str(maze[y][x]), True, BLACK)
            screen.blit(cell_text, (rect.centerx - cell_text.get_width()//2, rect.centery - cell_text.get_height()//2))
            
            pygame.draw.rect(screen, BLACK, rect, 1)

    a_rect = pygame.Rect(offset_x, offset_y + 5 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, a_rect, 0)
    a_text = font.render("A", True, WHITE)
    screen.blit(a_text, (a_rect.centerx - a_text.get_width()//2, a_rect.centery - a_text.get_height()//2))
    screen.blit(arrow_right_img, (offset_x - 30, offset_y + 5 * CELL_SIZE + 5))
    
    b_rect = pygame.Rect(offset_x + 4 * CELL_SIZE, offset_y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, b_rect, 0)
    b_text = font.render("B", True, WHITE)
    screen.blit(b_text, (b_rect.centerx - b_text.get_width()//2, b_rect.centery - b_text.get_height()//2))
    screen.blit(arrow_down_img, (offset_x + 4 * CELL_SIZE + 5, offset_y - 30))
    
    c_rect = pygame.Rect(offset_x + 12 * CELL_SIZE, offset_y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, c_rect, 0)
    c_text = font.render("C", True, WHITE)
    screen.blit(c_text, (c_rect.centerx - c_text.get_width()//2, c_rect.centery - c_text.get_height()//2))
    screen.blit(arrow_down_img, (offset_x + 12 * CELL_SIZE + 5, offset_y - 30))
    
    d_rect = pygame.Rect(offset_x + 13 * CELL_SIZE, offset_y + 5 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, d_rect, 0)
    d_text = font.render("D", True, WHITE)
    screen.blit(d_text, (d_rect.centerx - d_text.get_width()//2, d_rect.centery - d_text.get_height()//2))
    screen.blit(arrow_left_img, (offset_x + 14 * CELL_SIZE, offset_y + 5 * CELL_SIZE + 5))
    
    e_rect = pygame.Rect(offset_x + 4 * CELL_SIZE, offset_y + 10 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, e_rect, 0)
    e_text = font.render("E", True, WHITE)
    screen.blit(e_text, (e_rect.centerx - e_text.get_width()//2, e_rect.centery - e_text.get_height()//2))
    screen.blit(arrow_up_img, (offset_x + 4 * CELL_SIZE + 5, offset_y + 11 * CELL_SIZE))
    
    start_x = offset_x + 6 * CELL_SIZE + CELL_SIZE//2
    start_y = offset_y + 5 * CELL_SIZE + CELL_SIZE//2
    pygame.draw.line(screen, YELLOW, (start_x - 10, start_y - 10), (start_x + 10, start_y + 10), 3)
    pygame.draw.line(screen, YELLOW, (start_x + 10, start_y - 10), (start_x - 10, start_y + 10), 3)
    
    goal_rect = pygame.Rect(offset_x + 13 * CELL_SIZE, offset_y + 9 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(cup_img, goal_rect)

def draw_characters(game_manager, offset_x, offset_y):
    good_char = game_manager.get_good_character()
    good_loc = good_char.get_location()
    good_rect = pygame.Rect(offset_x + good_loc.get_x() * CELL_SIZE, offset_y + good_loc.get_y() * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    
    if good_char.get_name() == "Luke Skywalker":
        screen.blit(luke_game_img, good_rect)
    else:
        screen.blit(yoda_game_img, good_rect)
    
    for bad_char in game_manager.get_bad_characters():
        bad_loc = bad_char.get_location()
        bad_rect = pygame.Rect(offset_x + bad_loc.get_x() * CELL_SIZE, offset_y + bad_loc.get_y() * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        if bad_char.get_name() == "Darth Vader":
            screen.blit(vader_img, bad_rect)
        elif bad_char.get_name() == "Kylo Ren":
            screen.blit(kylo_img, bad_rect)
        else:
            screen.blit(trooper_img, bad_rect)
    
    goal_loc = game_manager.get_goal_location()
    goal_rect = pygame.Rect(offset_x + goal_loc.get_x() * CELL_SIZE, offset_y + goal_loc.get_y() * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(cup_img, goal_rect)

def draw_path_info(game_manager, offset_x, offset_y):
    """
    En kısa yol bilgisini ekranın sol altına çizer
    """
    path_info = game_manager.get_shortest_path_info()
    if path_info:
        shortest = min(path_info, key=lambda x: x[1])
        char_name = shortest[0]
        steps = shortest[1]
        
        if char_name == "Darth Vader":
            char_name = "Darth Vader"
        elif char_name == "Kylo Ren":
            char_name = "Kylo Ren"
        else:
            char_name = "Stormtrooper"
        
        text = f"En yakın: {char_name} ({steps} adım)"
        text_surface = font.render(text, True, DARK_RED)
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 40))

def draw_lives_info(game_manager, offset_x, offset_y):
    text = font.render("Canlar:", True, BLACK)
    screen.blit(text, (offset_x, offset_y))
    
    good_char = game_manager.get_good_character()
    lives = good_char.get_lives()
    
    if good_char.get_name() == "Luke Skywalker":
        for i in range(int(lives)):
            screen.blit(heart_full_img, (offset_x + 80 + i * 35, offset_y))
        for i in range(int(lives), 3):
            screen.blit(heart_empty_img, (offset_x + 80 + i * 35, offset_y))
    else:
        full_hearts = int(lives)
        half_heart = lives % 1 >= 0.5
        
        for i in range(full_hearts):
            screen.blit(heart_full_img, (offset_x + 80 + i * 35, offset_y))
        
        if half_heart:
            screen.blit(heart_half_img, (offset_x + 80 + full_hearts * 35, offset_y))
        
        empty_start = full_hearts + (1 if half_heart else 0)
        for i in range(empty_start, 3):
            screen.blit(heart_empty_img, (offset_x + 80 + i * 35, offset_y))

def game_over_screen(won=False):
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen
    running = True
    
    if yakalanma_sound:
        yakalanma_sound.play(-1)
    
    while running:
        screen.fill(BLACK)
        if won:
            title = large_font.render("TEBRİKLER!", True, GREEN)
            subtitle = font.render("Kupayı kazandın!", True, GREEN)
        else:
            title = large_font.render("GAME OVER", True, RED)
            subtitle = font.render("Kötü karakterler seni yakaladı!", True, RED)
        
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        restart_text = font.render("Yeniden başlamak için R tuşuna basın", True, YELLOW)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        menu_text = font.render("Ana menüye dönmek için M tuşuna basın", True, YELLOW)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if yakalanma_sound:
                        yakalanma_sound.stop()
                    return "restart"
                elif event.key == pygame.K_m:
                    if yakalanma_sound:
                        yakalanma_sound.stop()
                    return "menu"

def game_loop():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen
    running = True
    in_menu = True
    game_manager = None
    
    while running:
        if in_menu:
            character = character_selection_screen()
            if character:
                game_manager = GameManager("Star wars harita.txt")
                game_manager.select_character(character)
                in_menu = False
        else:
            screen.fill(LIGHT_BLUE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    if not (screen.get_flags() & pygame.FULLSCREEN):
                        SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game_manager.move_player("up")
                    elif event.key == pygame.K_DOWN:
                        game_manager.move_player("down")
                    elif event.key == pygame.K_LEFT:
                        game_manager.move_player("left")
                    elif event.key == pygame.K_RIGHT:
                        game_manager.move_player("right")
                    elif event.key == pygame.K_r and (game_manager.is_game_over() or game_manager.is_win()):
                        in_menu = True
                        continue
            
            draw_lives_info(game_manager, SCREEN_WIDTH // 2 - 80, 20)
            
            maze = game_manager.get_maze()
            offset_x = (SCREEN_WIDTH - len(maze[0]) * CELL_SIZE) // 2
            offset_y = (SCREEN_HEIGHT - len(maze) * CELL_SIZE) // 2 + 20
            
            draw_maze(maze, offset_x, offset_y, game_manager)
            draw_characters(game_manager, offset_x, offset_y)
            
            draw_path_info(game_manager, offset_x, offset_y)
            
            if game_manager.is_game_over() or game_manager.is_win():
                result = game_over_screen(game_manager.is_win())
                if result == "restart":
                    game_manager = GameManager("Star wars harita.txt")
                    game_manager.select_character(character)
                elif result == "menu":
                    in_menu = True
        
        pygame.display.flip()
        pygame.time.Clock().tick(10)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
