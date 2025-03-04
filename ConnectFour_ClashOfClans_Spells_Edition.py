import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 700, 750  # Increased height for spell menu
GRID_SIZE = 100
ROWS, COLS = 6, 7
PLAYER_COLORS = {"X": (255, 0, 0), "O": (0, 0, 255)}  # Red and Blue
SPELLS = ["Lightning", "Freeze", "Heal", "Jump", "Earthquake"]  # Shortened names for icons
SPELL_COLORS = {"Lightning": (255, 255, 0), "Freeze": (0, 255, 255), "Heal": (0, 255, 0), 
                "Jump": (255, 165, 0), "Earthquake": (139, 69, 19)}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4: Clash of Clans Spells Edition")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Load sound effects (only for token drop)
pygame.mixer.init()
drop_sound = pygame.mixer.Sound("drop.mp3")  # Add a sound file for token drop

# Create the board
def create_board():
    return [[None for _ in range(COLS)] for _ in range(ROWS)]

# Draw the board
def draw_board(board):
    screen.fill((0, 0, 0))  # Black background
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, (0, 0, 255), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)
            if board[row][col]:
                pygame.draw.circle(screen, PLAYER_COLORS[board[row][col]], 
                                 (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 5)

# Draw spell menu
def draw_spell_menu(player, spells, selected_spell):
    y_offset = HEIGHT - 100
    pygame.draw.rect(screen, (50, 50, 50), (0, y_offset, WIDTH, 100))  # Spell menu background
    for i, spell in enumerate(SPELLS):
        color = SPELL_COLORS[spell] if spell != selected_spell else (255, 255, 255)  # Highlight selected spell
        spell_text = font.render(f"{spell[0]}", True, color)  # Use first letter as icon
        screen.blit(spell_text, (20 + i * 130, y_offset + 20))
        count_text = font.render(f"{spells[player][spell]}", True, color)
        screen.blit(count_text, (20 + i * 130, y_offset + 50))

# Drop token animation
def drop_token_animation(board, col, player):
    for row in range(ROWS):
        if board[row][col] is None:
            board[row][col] = player
            draw_board(board)
            pygame.display.flip()
            drop_sound.play()  # Play drop sound
            pygame.time.wait(100)  # Animation delay
            if row < ROWS - 1 and board[row + 1][col] is None:
                board[row][col] = None
    return True

# Spell effects
def cast_lightning(board, col):
    for row in range(ROWS):
        if board[row][col] is not None:
            board[row][col] = None
            for r in range(row, 0, -1):
                board[r][col] = board[r - 1][col]
            board[0][col] = None
            break
    # Lightning animation (yellow flash)
    flash = pygame.Surface((GRID_SIZE, GRID_SIZE * ROWS))
    flash.fill((255, 255, 0))
    screen.blit(flash, (col * GRID_SIZE, 0))
    pygame.display.flip()
    pygame.time.wait(200)  # Flash duration

def cast_freeze(board, col, frozen_columns):
    frozen_columns[col] = 2  # Freeze for 2 turns
    # Freeze animation (blue overlay)
    freeze_overlay = pygame.Surface((GRID_SIZE, GRID_SIZE * ROWS))
    freeze_overlay.set_alpha(128)  # Semi-transparent
    freeze_overlay.fill((0, 255, 255))
    screen.blit(freeze_overlay, (col * GRID_SIZE, 0))
    pygame.display.flip()
    pygame.time.wait(200)  # Overlay duration

def cast_heal(board, row, col):
    if board[row][col] is not None:
        board[row][col] = f"H{board[row][col]}"  # Mark as healed
    # Heal animation (green glow)
    pygame.draw.circle(screen, (0, 255, 0), 
                      (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 5, 5)
    pygame.display.flip()
    pygame.time.wait(200)  # Glow duration

def cast_jump(board, col1, col2):
    for row in range(ROWS):
        board[row][col1], board[row][col2] = board[row][col2], board[row][col1]
    # Jump animation (quick swap)
    draw_board(board)
    pygame.display.flip()
    pygame.time.wait(200)  # Swap duration

def cast_earthquake(board, col):
    for row in range(ROWS - 1, 0, -1):
        board[row][col] = board[row - 1][col]
    board[0][col] = None
    # Earthquake animation (shaking effect)
    for _ in range(5):
        screen.scroll(dx=random.randint(-5, 5), dy=random.randint(-5, 5))
        pygame.display.flip()
        pygame.time.wait(50)
    draw_board(board)

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

# Main game loop
def main():
    board = create_board()
    players = ["X", "O"]
    spells = {
        "X": {"Lightning": 1, "Freeze": 1, "Heal": 1, "Jump": 1, "Earthquake": 1},
        "O": {"Lightning": 1, "Freeze": 1, "Heal": 1, "Jump": 1, "Earthquake": 1},
    }
    frozen_columns = {}  # Track frozen columns and their remaining freeze time
    turn = 0
    running = True
    selected_spell = None  # Track which spell is selected
    spell_target = None  # Track the target column/row for the selected spell

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                player = players[turn % 2]
                x, y = pygame.mouse.get_pos()

                if y < HEIGHT - 100:  # Clicked on the board
                    col = x // GRID_SIZE
                    if col < COLS:
                        if selected_spell is None:  # Drop token
                            if drop_token_animation(board, col, player):
                                if check_win(board, player):
                                    print(f"Player {player} wins!")
                                    running = False
                                turn += 1
                        else:  # Use spell
                            if selected_spell == "Lightning":
                                cast_lightning(board, col)
                            elif selected_spell == "Freeze":
                                cast_freeze(board, col, frozen_columns)
                            elif selected_spell == "Heal":
                                row = y // GRID_SIZE
                                cast_heal(board, row, col)
                            elif selected_spell == "Jump":
                                if spell_target is None:  # First column to swap
                                    spell_target = col
                                else:  # Second column to swap
                                    cast_jump(board, spell_target, col)
                                    spell_target = None
                            elif selected_spell == "Earthquake":
                                cast_earthquake(board, col)
                            selected_spell = None  # Reset selected spell
                else:  # Clicked on the spell menu
                    spell_index = (x - 20) // 130
                    if 0 <= spell_index < len(SPELLS):
                        selected_spell = SPELLS[spell_index]
                        if spells[player][selected_spell] > 0:
                            print(f"Player {player} selected {selected_spell}!")
                            spells[player][selected_spell] -= 1
                        else:
                            selected_spell = None  # No more uses of this spell

        draw_board(board)
        draw_spell_menu(players[turn % 2], spells, selected_spell)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()