import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 700, 700  # Increased height for spell menu
GRID_SIZE = 100
ROWS, COLS = 6, 7
PLAYER_COLORS = {"X": (255, 0, 0), "O": (0, 0, 255)}  # Red and Blue
SPELLS = ["Lightning", "Freeze", "Heal", "Jump", "Earthquake"]
SPELL_COLORS = {"Lightning": (255, 255, 0), "Freeze": (0, 255, 255), "Heal": (0, 255, 0), 
                "Jump": (255, 165, 0), "Earthquake": (139, 69, 19)}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4: Clash of Clans Spells Edition")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

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
def draw_spell_menu(player, spells):
    y_offset = HEIGHT - 100
    pygame.draw.rect(screen, (50, 50, 50), (0, y_offset, WIDTH, 100))  # Spell menu background
    for i, spell in enumerate(SPELLS):
        spell_text = font.render(f"{spell}: {spells[player][spell]}", True, SPELL_COLORS[spell])
        screen.blit(spell_text, (20 + i * 130, y_offset + 20))

# Drop token animation
def drop_token_animation(board, col, player):
    for row in range(ROWS):
        if board[row][col] is None:
            board[row][col] = player
            draw_board(board)
            pygame.display.flip()
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

def cast_freeze(board, col, frozen_columns):
    frozen_columns[col] = 2  # Freeze for 2 turns

def cast_heal(board, row, col):
    if board[row][col] is not None:
        board[row][col] = f"H{board[row][col]}"  # Mark as healed

def cast_jump(board, col1, col2):
    for row in range(ROWS):
        board[row][col1], board[row][col2] = board[row][col2], board[row][col1]

def cast_earthquake(board, col):
    for row in range(ROWS - 1, 0, -1):
        board[row][col] = board[row - 1][col]
    board[0][col] = None

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
                        if drop_token_animation(board, col, player):
                            if check_win(board, player):
                                print(f"Player {player} wins!")
                                running = False
                            turn += 1
                else:  # Clicked on the spell menu
                    spell_index = (x - 20) // 130
                    if 0 <= spell_index < len(SPELLS):
                        selected_spell = SPELLS[spell_index]
                        if spells[player][selected_spell] > 0:
                            print(f"Player {player} cast {selected_spell}!")
                            spells[player][selected_spell] -= 1
                            # Implement spell effects here
                            if selected_spell == "Lightning":
                                col = int(input("Choose a column to strike: "))  # Replace with mouse input
                                cast_lightning(board, col)
                            elif selected_spell == "Freeze":
                                col = int(input("Choose a column to freeze: "))  # Replace with mouse input
                                cast_freeze(board, col, frozen_columns)
                            elif selected_spell == "Heal":
                                row = int(input("Choose the row of the token to heal: "))  # Replace with mouse input
                                col = int(input("Choose the column of the token to heal: "))  # Replace with mouse input
                                cast_heal(board, row, col)
                            elif selected_spell == "Jump":
                                col1 = int(input("Choose the first column to swap: "))  # Replace with mouse input
                                col2 = int(input("Choose the second column to swap: "))  # Replace with mouse input
                                cast_jump(board, col1, col2)
                            elif selected_spell == "Earthquake":
                                col = int(input("Choose a column to earthquake: "))  # Replace with mouse input
                                cast_earthquake(board, col)
                            selected_spell = None  # Reset selected spell

        draw_board(board)
        draw_spell_menu(players[turn % 2], spells)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()