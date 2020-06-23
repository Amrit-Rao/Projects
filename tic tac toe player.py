import tkinter as tk
from tkinter import messagebox

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
buttons = [[tk.Button()] * 3 for y in range(3)]
turn = 0
play = ' '

GREEN = "#00FF00"
BLUE = "#0000FF"
WHITE = "#FFFFFF"


def intro(move):
    global play
    play = 'X' if move == 'X' else 'O'
    root_game.deiconify()
    root_intro.withdraw()


def clear():
    global turn, board, buttons
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
            buttons[i][j].config(text=board[i][j], state='normal')
    turn = 0
    root_game.withdraw()
    root_intro.deiconify()


def action(row, column):
    global turn, board, buttons
    symbol = 'X' if turn % 2 == 0 else 'O'
    board[row][column] = symbol
    buttons[row][column].config(text=board[row][column], state='disabled')
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            messagebox.showinfo(None, f"{symbol} wins!")
            clear()
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            messagebox.showinfo(None, f"{symbol} wins!")
            clear()
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        messagebox.showinfo(None, f"{symbol} wins!")
        clear()
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        messagebox.showinfo(None, f"{symbol} wins!")
        clear()
    turn += 1
    if turn == 9:
        messagebox.showinfo(None, f"Draw!")
        clear()


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

first_button = tk.Button(Frame_intro, command=lambda i='X': intro(i), text=f"First")
first_button.place(x=50, y=60, width=50, height=30)

second_button = tk.Button(Frame_intro, command=lambda i='O': intro(i), text=f"Second")
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
