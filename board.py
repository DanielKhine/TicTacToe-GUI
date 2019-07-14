import tkinter as tk

# variables
Width, Height = 400, 500
loop, scale = 3, 0.33

# game board class, subclass of Tk
class GameBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        # size of window is control by canvas.
        self.canvas = tk.Canvas(self, width=Width, height=Height)
        self.background_image = tk.PhotoImage(file='img/iwallpaper.png')
        self.background_label = tk.Label(self, image=self.background_image)

        # frame and label to show game information
        self.noti_frame = tk.Frame(self, bg="#391991", bd=10)
        self.noti_label = tk.Label(self.noti_frame, font=("Bauhaus 93", 20), bg="#070814", fg="#fff")
        self.frame = tk.Frame(self, bg='#391991', bd=10)

        # create a butoon to change which player go first
        self.mode_frame = tk.Frame(self, bg="#391991", bd=3)
        self.mode_btn1 = tk.Button(self.mode_frame, text="X", font=("Bauhaus 93", 20),
        command=lambda: self.btn_mode1(), bg="#070814", fg="aqua", relief=tk.GROOVE)

        # create a button for AI mode (coming soon...)
        self.mode_btn2 = tk.Button(self.mode_frame, text="AI", font=("Bauhaus 93", 20),
        command=lambda: self.restart(), bg="#070814", fg="#fff", relief=tk.GROOVE)
        self.mode_btn2.config(state=tk.DISABLED)

        # create a button to restart the game
        self.rest_frame = tk.Frame(self, bg="#391991", bd=6)
        self.rest_btn = tk.Button(self.rest_frame, text="Reset", font=("Bauhaus 93", 14),
        command=lambda: self.restart(), bg="#161626", fg="#fff", relief=tk.GROOVE)

        # initialize the game data / and update the game screen
        self.initialize_Val()
        self.initialize_Elements()
        self.update_elements()

    def initialize_Elements(self):
        '''this function create 9 buttons and store its in btn_list.
            Return- None
        '''
        self.frame_list = []
        self.btn_list = []
        for i in range(loop):
            self.frame_temp, self.btn_temp = [], []
            for j in range(loop):
                self.frame_temp.append(self.create_Btnframe())
                self.btn_temp.append(self.create_btn(self.frame_temp[j], i, j))
            # rank 2
            self.frame_list.append(self.frame_temp)
            self.btn_list.append(self.btn_temp)

    def create_Btnframe(self):
        ''' this function return tk frame object.
        '''
        return tk.Frame(self.frame, bg='#391991', bd=0)

    def create_btn(self, parent, i, j):
        ''' this function return tk button object.
        '''
        return tk.Button(parent, text=" ", font=("Microsoft YaHei UI Light", 40),
         command=lambda: self.btn_click(i, j), bg='#161626', fg='aqua', relief=tk.GROOVE)

    def btn_click(self, i, j):
        ''' this function hendle button click events of buttons in btn_list,
            and update the game screen.
        '''
        if self.board_lst[i][j] ==' ' and self.End != 1:
            # assign player & change color
            self.btn_list[i][j]["fg"] = self.pColor[self.turn]
            self.board_lst[i][j] = self.player[self.turn]
            self.End = self.check_for_winner()
            if self.End == -1:
                self.turn = (self.turn + 1) % 2
            self.update_elements()

    def btn_mode1(self):
        if len(self.get_open_spots()) == 9:
            self.turn = (self.turn + 1) % 2
            self.mode_btn1["fg"] = self.pColor[self.turn]
            self.mode_btn1["text"] = self.player[self.turn]
            self.update_elements()

    # coming soon...
    def btn_mode2(self):
        if len(self.get_open_spots()) == 9:
            pass

    def update_elements(self):
        ''' update the game screen.
        '''
        # board_lst is rank 2 list [[X,O, ],[O, ,O],etc...]
        for i in range(loop):
            for j in range(loop):
                self.btn_list[i][j]["text"] = self.board_lst[i][j]
        if self.End == -1:
            self.noti_label["text"] = "Player " + self.player[self.turn] + " turn"
        elif self.End:
            self.noti_label["fg"] = self.pColor[self.turn]
            self.noti_label["text"] = "Player " + self.player[self.turn] + " Win!"
        else:
            self.noti_label["text"] = "Draw!"

    def render(self):
        ''' Show all the game elements.
        '''
        self.background_label.place(relwidth=1, relheight=1)
        self.canvas.pack()
        self.noti_frame.place(relx=0.5, rely=0.02, relwidth=0.9, relheight=0.15, anchor='n')
        self.noti_label.place(relwidth=1, relheight=1)
        self.frame.place(relx=0.5, rely=0.18, relwidth=0.9, relheight=0.7, anchor='n')
        self.mode_frame.place(relx=0.5, rely=0.89, relwidth=0.3, relheight=0.1, anchor='n')
        self.mode_btn1.place(relwidth=0.5, relheight=1)
        self.mode_btn2.place(relx=0.5, relwidth=0.5, relheight=1)
        self.rest_frame.place(relx=0.8, rely=0.89, relwidth=0.3, relheight=0.1, anchor='n')
        self.rest_btn.place(relwidth=0.95, relheight=1)
        # render all frame buttons
        for i in range(loop):
            for j in range(loop):
                self.frame_list[i][j].place(relx=j * scale, rely=i * scale, relwidth=scale, relheight=scale)
                self.btn_list[i][j].place(relwidth=1, relheight=1)


    #--------------Game logics------------------#

    def initialize_Val(self):
        ''' Initialize the game variables.
        '''
        self.board_lst = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.turn = 0
        self.player = ["X", "O"]
        self.pColor = ["aqua", "magenta"]
        self.End = -1

    def restart(self):
        ''' Restart the game.
        '''
        self.initialize_Val()
        self.update_elements()
        self.noti_label["fg"] = "#fff"
        self.mode_btn1["fg"] = self.pColor[self.turn]
        self.mode_btn1["text"] = self.player[self.turn]

    def get_open_spots(self):
        ''' this function return list of avaliable position in game board.
            Note: only use to check 'Draw' or not.
        '''
        return [[r,c] for r in range(3) for c in range(3) if self.board_lst[r][c] == ' ']

    def check_for_winner(self):
        ''' Check the winner.Return: '1' if one player win,'-1' to continue the game.'0' if nobody win.
        '''
        for c in range(3):
            if self.board_lst[0][c] == self.board_lst[1][c] == self.board_lst[2][c] != ' ':
                return 1
        for r in range(3):
            if self.board_lst[r][0] == self.board_lst[r][1] == self.board_lst[r][2] != ' ':
                return 1
        if self.board_lst[0][0] == self.board_lst[1][1] == self.board_lst[2][2] != ' ':
            return True
        if self.board_lst[2][0] == self.board_lst[1][1] == self.board_lst[0][2] != ' ':
            return 1
        if self.get_open_spots() == []:
            return 0
        return -1


####################TST#####################
if __name__ == "__main__":
    app = GameBoard()
    app.resizable(0, 0)
    app.title("Tic-tac-toe")
    app.render()
    app.mainloop()
