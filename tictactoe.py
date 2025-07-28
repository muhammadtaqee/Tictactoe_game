import pygame
import sys
import random
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Constants
WIDTH, HEIGHT = 800, 600
BOARD_SIZE = 300
BOARD_POS = (WIDTH // 2 - BOARD_SIZE // 2, HEIGHT // 2 - BOARD_SIZE // 2 + 50)
CELL_SIZE = BOARD_SIZE // 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
PURPLE = (150, 50, 200)
YELLOW = (255, 255, 0)

# Game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Tic-Tac-Toe")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Arial", 50, bold=True)
main_font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 20)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
current_state = MENU

# Game data
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None
game_mode = "PvP"  # "PvP" or "PvAI"
player1_name = "Player 1"
player2_name = "Player 2" if game_mode == "PvP" else "AI"
scores = {"X": 0, "O": 0}
game_history = []
ai_difficulty = "medium"  # "easy", "medium", "hard"

# Load sounds
try:
    click_sound = mixer.Sound("click.wav")
    win_sound = mixer.Sound("win.wav")
    draw_sound = mixer.Sound("draw.wav")
except:
    print("Sound files not found. Continuing without sound.")

def draw_menu():
    screen.fill(WHITE)
    
    # Title
    title_text = title_font.render("TIC-TAC-TOE", True, BLUE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Game mode selection
    pygame.draw.rect(screen, GRAY if game_mode == "PvP" else BLUE, 
                    (WIDTH // 2 - 150, 150, 300, 50))
    mode_text = main_font.render("Player vs Player", True, BLACK if game_mode == "PvP" else WHITE)
    screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, 160))
    
    pygame.draw.rect(screen, GRAY if game_mode == "PvAI" else BLUE, 
                    (WIDTH // 2 - 150, 220, 300, 50))
    mode_text = main_font.render("Player vs AI", True, BLACK if game_mode == "PvAI" else WHITE)
    screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, 230))
    
    # AI difficulty (only visible in PvAI mode)
    if game_mode == "PvAI":
        diff_colors = {
            "easy": GRAY if ai_difficulty == "easy" else BLUE,
            "medium": GRAY if ai_difficulty == "medium" else BLUE,
            "hard": GRAY if ai_difficulty == "hard" else BLUE
        }
        
        pygame.draw.rect(screen, diff_colors["easy"], (WIDTH // 2 - 150, 290, 90, 40))
        diff_text = small_font.render("Easy", True, BLACK if ai_difficulty == "easy" else WHITE)
        screen.blit(diff_text, (WIDTH // 2 - 150 + 45 - diff_text.get_width() // 2, 300))
        
        pygame.draw.rect(screen, diff_colors["medium"], (WIDTH // 2 - 50, 290, 100, 40))
        diff_text = small_font.render("Medium", True, BLACK if ai_difficulty == "medium" else WHITE)
        screen.blit(diff_text, (WIDTH // 2 - 50 + 50 - diff_text.get_width() // 2, 300))
        
        pygame.draw.rect(screen, diff_colors["hard"], (WIDTH // 2 + 60, 290, 90, 40))
        diff_text = small_font.render("Hard", True, BLACK if ai_difficulty == "hard" else WHITE)
        screen.blit(diff_text, (WIDTH // 2 + 60 + 45 - diff_text.get_width() // 2, 300))
    
    # Start button
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, 370, 200, 60))
    start_text = main_font.render("START GAME", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 385))
    
    # Player names input
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, 450, 300, 40), 2)
    name_text = small_font.render(player1_name, True, BLACK)
    screen.blit(name_text, (WIDTH // 2 - 140, 460))
    
    if game_mode == "PvP":
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, 500, 300, 40), 2)
        name_text = small_font.render(player2_name, True, BLACK)
        screen.blit(name_text, (WIDTH // 2 - 140, 510))

def draw_game():
    screen.fill(WHITE)
    
    # Draw scores
    pygame.draw.rect(screen, BLUE, (50, 20, 200, 60))
    score_text = main_font.render(f"{player1_name}: {scores['X']}", True, WHITE)
    screen.blit(score_text, (150 - score_text.get_width() // 2, 40))
    
    pygame.draw.rect(screen, RED, (WIDTH - 250, 20, 200, 60))
    score_text = main_font.render(f"{player2_name}: {scores['O']}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150 - score_text.get_width() // 2, 40))
    
    # Draw current turn indicator
    turn_color = BLUE if current_player == "X" else RED
    pygame.draw.circle(screen, turn_color, (WIDTH // 2, 50), 15)
    turn_text = main_font.render("Current Turn", True, BLACK)
    screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 70))
    
    # Draw board
    pygame.draw.rect(screen, BLACK, (*BOARD_POS, BOARD_SIZE, BOARD_SIZE), 3)
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, 
                        (BOARD_POS[0], BOARD_POS[1] + i * CELL_SIZE),
                        (BOARD_POS[0] + BOARD_SIZE, BOARD_POS[1] + i * CELL_SIZE), 3)
        pygame.draw.line(screen, BLACK, 
                        (BOARD_POS[0] + i * CELL_SIZE, BOARD_POS[1]),
                        (BOARD_POS[0] + i * CELL_SIZE, BOARD_POS[1] + BOARD_SIZE), 3)
    
    # Draw X's and O's
    for row in range(3):
        for col in range(3):
            center_x = BOARD_POS[0] + col * CELL_SIZE + CELL_SIZE // 2
            center_y = BOARD_POS[1] + row * CELL_SIZE + CELL_SIZE // 2
            
            if board[row][col] == "X":
                pygame.draw.line(screen, BLUE, 
                                (center_x - 30, center_y - 30),
                                (center_x + 30, center_y + 30), 5)
                pygame.draw.line(screen, BLUE, 
                                (center_x + 30, center_y - 30),
                                (center_x - 30, center_y + 30), 5)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, RED, (center_x, center_y), 30, 5)
    
    # Draw winning line if game is over
    if winner:
        draw_winning_line()
    
    # Draw menu button
    pygame.draw.rect(screen, PURPLE, (WIDTH // 2 - 80, HEIGHT - 70, 160, 40))
    menu_text = small_font.render("Main Menu", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT - 60))

def draw_game_over():
    screen.fill(WHITE)
    
    # Game over message
    if winner == "draw":
        result_text = title_font.render("It's a Draw!", True, PURPLE)
    else:
        winner_name = player1_name if winner == "X" else player2_name
        result_text = title_font.render(f"{winner_name} Wins!", True, GREEN if winner == "X" else RED)
    
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 100))
    
    # Scoreboard
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 150, 200, 300, 60))
    score_text = main_font.render(f"{player1_name}: {scores['X']}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 220))
    
    pygame.draw.rect(screen, RED, (WIDTH // 2 - 150, 280, 300, 60))
    score_text = main_font.render(f"{player2_name}: {scores['O']}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))
    
    # Game history
    history_text = main_font.render("Game History", True, BLACK)
    screen.blit(history_text, (WIDTH // 2 - history_text.get_width() // 2, 370))
    
    for i, result in enumerate(game_history[-5:]):  # Show last 5 games
        hist_y = 420 + i * 30
        if result == "draw":
            hist_msg = f"Game {len(game_history)-5+i+1}: Draw"
            color = PURPLE
        else:
            winner_name = player1_name if result == "X" else player2_name
            hist_msg = f"Game {len(game_history)-5+i+1}: {winner_name} won"
            color = GREEN if result == "X" else RED
        
        hist_text = small_font.render(hist_msg, True, color)
        screen.blit(hist_text, (WIDTH // 2 - hist_text.get_width() // 2, hist_y))
    
    # Play again button
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT - 120, 200, 50))
    again_text = main_font.render("Play Again", True, WHITE)
    screen.blit(again_text, (WIDTH // 2 - again_text.get_width() // 2, HEIGHT - 110))
    
    # Menu button
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, HEIGHT - 60, 200, 50))
    menu_text = main_font.render("Main Menu", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT - 50))

def draw_winning_line():
    # Find winning positions
    winning_positions = []
    
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            winning_positions = [(row, 0), (row, 1), (row, 2)]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            winning_positions = [(0, col), (1, col), (2, col)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        winning_positions = [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != "":
        winning_positions = [(0, 2), (1, 1), (2, 0)]
    
    # Draw the line
    if winning_positions:
        start_pos = (BOARD_POS[0] + winning_positions[0][1] * CELL_SIZE + CELL_SIZE // 2,
                    BOARD_POS[1] + winning_positions[0][0] * CELL_SIZE + CELL_SIZE // 2)
        end_pos = (BOARD_POS[0] + winning_positions[2][1] * CELL_SIZE + CELL_SIZE // 2,
                  BOARD_POS[1] + winning_positions[2][0] * CELL_SIZE + CELL_SIZE // 2)
        
        line_color = BLUE if winner == "X" else RED
        pygame.draw.line(screen, line_color, start_pos, end_pos, 8)

def check_winner():
    global winner
    
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            winner = board[row][0]
            return
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            winner = board[0][col]
            return
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        winner = board[0][0]
        return
    if board[0][2] == board[1][1] == board[2][0] != "":
        winner = board[0][2]
        return
    
    # Check for draw
    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        winner = "draw"

def make_move(row, col):
    global current_player
    
    if board[row][col] == "" and not winner:
        board[row][col] = current_player
        try:
            mixer.Sound.play(click_sound)
        except:
            pass
        
        check_winner()
        
        if not winner:
            current_player = "O" if current_player == "X" else "X"
            
            # AI move in PvAI mode
            if game_mode == "PvAI" and current_player == "O":
                ai_move()

def ai_move():
    if ai_difficulty == "easy":
        # Random moves
        empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            make_move(row, col)
    
    elif ai_difficulty == "medium":
        # Sometimes blocks or wins, sometimes random
        if random.random() < 0.7:  # 70% chance to make a smart move
            # Check for winning move
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "O"
                        check_winner()
                        board[r][c] = ""
                        if winner == "O":
                            make_move(r, c)
                            return
            
            # Check for blocking move
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "X"
                        check_winner()
                        board[r][c] = ""
                        if winner == "X":
                            make_move(r, c)
                            return
            
            # If no immediate win/block, choose randomly
            empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
            if empty_cells:
                row, col = random.choice(empty_cells)
                make_move(row, col)
        else:
            # 30% chance to make a random move
            empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
            if empty_cells:
                row, col = random.choice(empty_cells)
                make_move(row, col)
    
    elif ai_difficulty == "hard":
        # Minimax algorithm for unbeatable AI
        best_score = -float('inf')
        best_move = None
        
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "O"
                    score = minimax(board, 0, False)
                    board[r][c] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        
        if best_move:
            make_move(best_move[0], best_move[1])

def minimax(board, depth, is_maximizing):
    # Check terminal states
    check_winner()
    if winner == "O":
        return 10 - depth
    elif winner == "X":
        return depth - 10
    elif winner == "draw":
        return 0
    winner = None  # Reset winner check
    
    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "O"
                    score = minimax(board, depth + 1, False)
                    board[r][c] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "X"
                    score = minimax(board, depth + 1, True)
                    board[r][c] = ""
                    best_score = min(score, best_score)
        return best_score

def reset_game():
    global board, current_player, winner
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None

def handle_menu_click(pos):
    global game_mode, current_state, ai_difficulty
    
    # Game mode selection
    if WIDTH // 2 - 150 <= pos[0] <= WIDTH // 2 + 150:
        if 150 <= pos[1] <= 200:  # PvP
            game_mode = "PvP"
            player2_name = "Player 2"
        elif 220 <= pos[1] <= 270:  # PvAI
            game_mode = "PvAI"
            player2_name = "AI"
    
    # AI difficulty selection
    if game_mode == "PvAI" and 290 <= pos[1] <= 330:
        if WIDTH // 2 - 150 <= pos[0] <= WIDTH // 2 - 60:  # Easy
            ai_difficulty = "easy"
        elif WIDTH // 2 - 50 <= pos[0] <= WIDTH // 2 + 50:  # Medium
            ai_difficulty = "medium"
        elif WIDTH // 2 + 60 <= pos[0] <= WIDTH // 2 + 150:  # Hard
            ai_difficulty = "hard"
    
    # Start game button
    if WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and 370 <= pos[1] <= 430:
        reset_game()
        current_state = PLAYING

def handle_game_click(pos):
    global current_state
    
    # Board clicks
    if (BOARD_POS[0] <= pos[0] <= BOARD_POS[0] + BOARD_SIZE and
        BOARD_POS[1] <= pos[1] <= BOARD_POS[1] + BOARD_SIZE):
        col = (pos[0] - BOARD_POS[0]) // CELL_SIZE
        row = (pos[1] - BOARD_POS[1]) // CELL_SIZE
        make_move(row, col)
    
    # Menu button
    if WIDTH // 2 - 80 <= pos[0] <= WIDTH // 2 + 80 and HEIGHT - 70 <= pos[1] <= HEIGHT - 30:
        current_state = MENU

def handle_game_over_click(pos):
    global current_state
    
    # Play again button
    if WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and HEIGHT - 120 <= pos[1] <= HEIGHT - 70:
        reset_game()
        current_state = PLAYING
    
    # Menu button
    if WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and HEIGHT - 60 <= pos[1] <= HEIGHT - 10:
        current_state = MENU

def main():
    global current_state, winner, scores, game_history, current_player
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if current_state == MENU:
                    handle_menu_click(pos)
                elif current_state == PLAYING:
                    handle_game_click(pos)
                elif current_state == GAME_OVER:
                    handle_game_over_click(pos)
        
        # Check if game is over
        if current_state == PLAYING and winner:
            if winner != "draw":
                scores[winner] += 1
                try:
                    mixer.Sound.play(win_sound)
                except:
                    pass
            else:
                try:
                    mixer.Sound.play(draw_sound)
                except:
                    pass
            game_history.append(winner)
            current_state = GAME_OVER
        
        # Draw the appropriate screen
        if current_state == MENU:
            draw_menu()
        elif current_state == PLAYING:
            draw_game()
        elif current_state == GAME_OVER:
            draw_game_over()
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()