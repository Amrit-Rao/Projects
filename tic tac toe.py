import tkinter as tk
from tkinter import messagebox
import copy
import numpy as np

#Initialize 2 roots , one for game and one for player select
root_game = tk.Tk()
root_intro = tk.Tk()

screen_height = root_game.winfo_screenheight()
screen_width = root_game.winfo_screenwidth()

game_window_height = 400
game_window_width = 300

intro_window_width = 300
intro_window_height = 100

game_position_height = screen_height // 2 - game_window_height // 2
game_position_width = screen_width // 2 - game_window_width // 2

intro_position_height = screen_height // 2 - intro_window_height // 2
intro_position_width = screen_width // 2 - intro_window_width // 2

root_game.geometry(f"{game_window_width}x{game_window_height}+{game_position_width}+{game_position_height}")
root_intro.geometry(f"{intro_window_width}x{intro_window_height}+{intro_position_width}+{intro_position_height}")
root_game.resizable(0, 0)
root_intro.resizable(0, 0)

root_game.withdraw()

board = [[' '] * 3 for x in range(3)]
answer = [[' '] * 3 for y in range(3)]
buttons = [[tk.Button()] * 3 for z in range(3)]
turn = 0

GREEN = "#00FF00"
BLUE = "#0000FF"
WHITE = "#FFFFFF"

#Initial window to set the turn according to the player
def player_select(move):
    global turn
    turn = 1 if move == 'X' else 2
    root_game.deiconify()
    root_intro.withdraw()
    ai_plays()

#Clears the board
def clear():
    global board, buttons, answer
    for i in range(3):
        for j in range(3):
            board[i][j] = answer[i][j] = ' '
            buttons[i][j].config(text=board[i][j], state='normal')

    root_game.withdraw()
    root_intro.deiconify()

#Mark X and O appropriately on the board and display who wins
def action(row, column):
    global board, buttons, turn
    board[row][column] = 'X' if whose_turn(board) == 'X' else 'O'
    buttons[row][column].config(text=board[row][column], state='disabled')
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            messagebox.showinfo(None, f"Player wins!")
            clear()
            return
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            messagebox.showinfo(None, f"Player wins!")
            clear()
            return
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        messagebox.showinfo(None, f"Player wins!")
        clear()
        return
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        messagebox.showinfo(None, f"Player wins!")
        clear()
        return
    if is_full(board):
        messagebox.showinfo(None, f"Draw!")
        clear()
        return
    turn += 1
    ai_plays()

#Defines turn
def whose_turn(position):
    turn_helper = 0
    for i in range(3):
        for j in range(3):
            if position[i][j] != ' ':
                turn_helper += 1
    return 'X' if turn_helper % 2 == 0 else 'O'

#Checks whether the board is full(results in draw)
def is_full(position):
    for i in range(3):
        for j in range(3):
            if position[i][j] == ' ':
                return False
    return True

#Optimized function to play the first 2 moves, can work without this but will take some time
def forced_play(position):
    global answer
    move = 0
    for i in range(3):
        for j in range(3):
            if position[i][j] != ' ':
                move += 1
    if move == 0:
        chance = np.random.randint(13)
        if chance == 0:
            random_number_1 = np.random.randint(2) * 2
            random_number_2 = np.random.randint(2)
            if random_number_2 == 0:
                answer[random_number_1][1] = 'X'

            else:
                answer[1][random_number_1] = 'X'
        elif 1 <= chance <= 8:
            random_number_1 = np.random.randint(2) * 2
            random_number_2 = np.random.randint(2) * 2
            answer[random_number_1][random_number_2] = 'X'
        else:
            answer[1][1] = 'X'
        return True
    elif move == 1:
        row = 3
        column = 3
        for i in range(3):
            for j in range(3):
                if position[i][j] == 'X':
                    answer[i][j] = 'X'
                    row = i
                    column = j
                    break
        if row % 2 == column % 2 == 0:
            answer[1][1] = 'O'
        elif row == 1 and column == 1:
            random_number_1 = np.random.randint(2) * 2
            random_number_2 = np.random.randint(2) * 2
            answer[random_number_1][random_number_2] = 'O'
        else:
            chance = np.random.randint(13)
            if chance == 0:
                if row % 2 == 0:
                    new_row = 2 if row == 0 else 0
                    answer[new_row][column] = 'O'
                if column % 2 == 0:
                    new_column = 2 if column == 0 else 0
                    answer[row][new_column] = 'O'
            elif 1 <= chance <= 4:
                answer[1][1] = 'O'
            else:
                if row == 1:
                    new_row = np.random.randint(2) * 2
                    answer[new_row][column] = 'O'
                if column == 1:
                    new_column = np.random.randint(2) * 2
                    answer[row][new_column] = 'O'
        return True
    else:
        return False

#Get all possible plays from given board position
def get_plays(position):
    plays = []
    symbol = 'X' if whose_turn(position) == 'X' else 'O'
    for i in range(3):
        for j in range(3):
            if position[i][j] == ' ':
                plays.append(copy.deepcopy(position))
                plays[-1][i][j] = symbol
    return plays

#Checks for win 
def check_for_win(position):
    invert_symbol = 'O' if whose_turn(position) == 'X' else 'X'
    for i in range(3):
        if position[i][0] == position[i][1] == position[i][2] != ' ':
            return invert_symbol
        if position[0][i] == position[1][i] == position[2][i] != ' ':
            return invert_symbol
    if position[0][0] == position[1][1] == position[2][2] != ' ':
        return invert_symbol
    if position[0][2] == position[1][1] == position[2][0] != ' ':
        return invert_symbol
    return 'Draw'

#Solves using Minimax theorem
def solve(position):
    global answer
    if check_for_win(position) != 'Draw':
        return check_for_win(position)
    if is_full(position):
        return 'Draw'
    if forced_play(position):
        return 'Draw'
    plays = get_plays(position)
    check_play = np.array([solve(plays[i]) for i in range(len(plays))])
    x_wins = np.where(check_play == 'X')
    o_wins = np.where(check_play == 'O')
    draw = np.where(check_play == 'Draw')

    if whose_turn(position) == 'X':
        if 'X' in check_play:
            answer = plays[x_wins[-1][np.random.randint(len(x_wins[-1]))]]
            return 'X'

        elif 'Draw' in check_play:
            answer = plays[draw[-1][np.random.randint(len(draw[-1]))]]
            return 'Draw'
        else:
            answer = plays[o_wins[-1][np.random.randint(len(o_wins[-1]))]]
            return 'O'
    else:
        if 'O' in check_play:
            answer = plays[o_wins[-1][np.random.randint(len(o_wins[-1]))]]
            return 'O'
        elif 'Draw' in check_play:
            answer = plays[draw[-1][np.random.randint(len(draw[-1]))]]
            return 'Draw'
        else:
            answer = plays[x_wins[-1][np.random.randint(len(x_wins[-1]))]]
            return 'X'

#Function to play after the player has made their move through solve function
def ai_plays():
    global board, buttons, turn, answer
    if turn % 2 == 0:
        solve(board)
        for i in range(3):
            for j in range(3):
                board[i][j] = answer[i][j]
                buttons[i][j].config(text=board[i][j])
                if board[i][j] != ' ':
                    buttons[i][j].config(state='disabled')
        turn += 1
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                messagebox.showinfo(None, f"AI wins!")
                clear()
                return
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                messagebox.showinfo(None, f"AI wins!")
                clear()
                return
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            messagebox.showinfo(None, f"AI wins!")
            clear()
            return
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            messagebox.showinfo(None, f"AI wins!")
            clear()
            return
        if is_full(board):
            messagebox.showinfo(None, f"Draw!")
            clear()
            return

#Initialization of board
Frame_1 = tk.Frame(root_game, width=300, height=50)
Frame_2 = tk.Frame(root_game, width=300, height=300)
Frame_3 = tk.Frame(root_game, bg=GREEN, width=300, height=50)
Frame_intro = tk.Frame(root_intro, bg=BLUE, width=300, height=100)

Label_1 = tk.Label(Frame_1, bg=GREEN, width=300, font=("Arial", 20, "bold"), text=f"TIC TAC TOE")
Label_1.pack()

Label_2 = tk.Label(Frame_intro, bg=BLUE, font=("Arial", 20, "bold"), text=f"Which turn?")
Label_2.place(x=50, y=0, width=210, height=50)
 
reset_button = tk.Button(Frame_3, command=lambda: clear(), text=f"Reset")
reset_button.place(x=50, y=10, width=50, height=30)

quit_button_game = tk.Button(Frame_3, command=lambda: quit(), text=f"Quit")
quit_button_game.place(x=200, y=10, width=50, height=30)

quit_button_intro = tk.Button(Frame_intro, command=lambda: quit(), text=f"Quit")
quit_button_intro.place(x=200, y=60, width=50, height=30)

first_button = tk.Button(Frame_intro, command=lambda i='X': player_select(i), text=f"First")
first_button.place(x=50, y=60, width=50, height=30)

second_button = tk.Button(Frame_intro, command=lambda i='O': player_select(i), text=f"Second")
second_button.place(x=125, y=60, width=50, height=30)

Frame_1.pack(side="top")
Frame_3.pack(side="bottom")
Frame_2.pack()
Frame_intro.pack()

Color_helper = True

for a in range(3):
    Frame_2.columnconfigure(a, weight=1)
    for b in range(3):
        Frame_2.rowconfigure(b, weight=1)
        buttons[a][b] = tk.Button(Frame_2, command=lambda row=a, column=b: action(row, column),
                                  width=5, height=5, text=board[a][b], font=("arial", 50, "bold"))
        if Color_helper:
            buttons[a][b].config(bg=WHITE)
        else:
            buttons[a][b].config(bg=BLUE)
        buttons[a][b].grid(row=a, column=b)
        Color_helper = not Color_helper

root_game.mainloop()
