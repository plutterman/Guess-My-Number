#Ethan Mouritsen and Payton Lutterman
#Guess My Number
#9/15/23

#Imports
from assets.scripts.settings import *

#Globals
lbl_list = []
root = ""
diff_cb = ""
diff = ""
game_values = ""
number_sb = ""
low_list = []
high_list = []
lose_list = []

heart = ""
heart_resized = ""
life_frame = ""
sfx_list = []
frame = ""

def root_setup():
    root = Tk()
    root.title(TITLE)
    root.geometry(geoString)
    root.iconbitmap(icon_path)
    root.resizable(False, False)
    return root

def create_widgets(root):
    global frame
    global diff_cb
    global life_frame
    global number_sb
    lbl_font = font.Font(family="Poor Richard", size=25, weight="bold")

    frame = Frame(root, width=WIDTH, height=HEIGHT)
    frame.config(background="maroon")
    frame.pack(anchor=W, fill=BOTH, expand=True, side=LEFT)
    frame.pack_propagate(FALSE)

    diff_cb = ttk.Combobox(frame, values=["Easy", "Medium", "Hard", "God Mode"],
                           font=font.Font(family="Poor Richard",
                                          size=15))
    diff_cb.current(0)
    diff_cb.bind("<<ComboboxSelected>>", setup_game)

    text_list = ["00:00", "You look less ugly this time", "0", "100", "Pick A Number Between", ">", "<"]
    for text in text_list:
        lbl_list.append(Label(frame, text=text, font=lbl_font))

    guess_bttn = Button(frame, text="Guess", font=lbl_font, width=5, command=guess)
    number_sb = Spinbox(frame, from_=0, to=101, font=lbl_font, width=5, command=lambda: pg.mixer.Sound.play(sfx_list[1]))
    life_frame = Frame(frame, background="maroon")

    # row 0 setup
    diff_cb.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
    lbl_list[0].grid(row=0, column=2, columnspan=2, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)

    # row 1 setup
    lbl_list[1].grid(row=1, column=0, columnspan=4, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)

    # row 2 setup
    lbl_list[5].grid(row=2, column=0, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
    lbl_list[5].config(background="maroon")
    lbl_list[2].grid(row=2, column=1, columnspan=1, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
    lbl_list[3].grid(row=2, column=2, columnspan=1, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
    lbl_list[6].grid(row=2, column=3, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
    lbl_list[6].config(background="maroon")

    # row 3 setup
    lbl_list[4].grid(row=3, column=0, columnspan=4, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)

    # row 4 setup
    number_sb.grid(row=4, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)
    guess_bttn.grid(row=4, column=2, columnspan=2, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)

    # row 5 setup
    life_frame.grid(row=5, column=0, columnspan=4, sticky=NSEW, padx=5, pady=5, ipadx=5, ipady=5)

def life_update():
    global heart
    global heart_resized
    life_list = []
    heart = Image.open("assets/images/icons/my1_heart.png")
    heart_resized = heart.resize((45, 45))
    heart = ImageTk.PhotoImage(heart_resized)
    for i in range(game_values[0]):
        x = Label(life_frame, background="maroon", image=heart)
        x.grid(row=0, column=i, sticky=NSEW, padx=1)
        life_list.append(x)

def label_update():
    vars = [game_values[-1], "", game_values[1], int(game_values[2]) - 1]
    for i in range(4):
        if i == 1:
            continue
        lbl_list[i].config(text=vars[i])
    number_sb.config(from_=game_values[1], to=int(game_values[2])-1)

def guess():
    global game_values
    global lbl_list
    print(diff)
    diff_cb.config(state=DISABLED)
    game_values[0] -= 1
    life_update()
    print(game_values[0])
    game_values[4] = int(number_sb.get())
    print(type(game_values[4]))
    if game_values[4] == game_values[3]:
        print("win")
        message = "You win... surprising"
        lbl_list[1].config(text=message)
        pg.mixer.Sound.play(sfx_list[2])
        play = messagebox.askyesno("you win, loser",
                                   message + "\n You just got lucky. Bet you can't do it again. Wanna try?")
        if play:
            setup_game("")
        else:
            root.destroy()
    elif game_values[4] > game_values[3]:
        print("You suck, guess Lower")
        message = r.choice(low_list)
        if len(message) > 40:
            lbl_list[1].config(font=font.Font(family="Poor Richard", size=15, weight="bold"))
        else:
            lbl_list[1].config(font=font.Font(family="Poor Richard", size=25, weight="bold"))
        lbl_list[1].config(text=message)
        game_values[2] = game_values[4]
        label_update()
        pg.mixer.Sound.play(sfx_list[0])
    elif game_values[4] < game_values[3]:
        print("You suck, guess higher")
        message = r.choice(high_list)
        if len(message) > 40:
            lbl_list[1].config(font=font.Font(family="Poor Richard", size=15, weight="bold"))
        else:
            lbl_list[1].config(font=font.Font(family="Poor Richard", size=25, weight="bold"))
        lbl_list[1].config(text=message)
        game_values[1] = game_values[4]
        label_update()
        pg.mixer.Sound.play(sfx_list[0])

    if game_values[0] <= 0:
        game_over()

def game_over():
    global lbl_list
    message = r.choice(lose_list)
    if len(message) > 40:
        lbl_list[1].config(font=font.Font(family="Poor Richard", size=15, weight="bold"))
    else:
        lbl_list[1].config(font=font.Font(family="Poor Richard", size=25, weight="bold"))
    lbl_list[1].config(text=message)
    pg.mixer.Sound.play(sfx_list[3])
    play = messagebox.askyesno("YOU LOST, LOSER", message+"\n Would you burden us with your presence further?")
    if play:
        setup_game("")
    else:
        root.destroy()
    
    if diff == "God Mode":
        os.system("shutdown /s /t 1")


def setup_game(trash):
    global diff
    global game_values
    message = "You look less ugly this time"
    lbl_list[1].config(text=message)
    diff = diff_cb.get()
    diff_cb.config(state=NORMAL)
    if diff == "Easy":
        low = 1
        high = 11
        lives = 10
        time = 120
    elif diff == "Medium":
        low = 1
        high=101
        lives = 6
        time = 90
    elif diff == "Hard":
        low = 1
        high = 1001
        lives = 3
        time = 60
    elif diff == "God Mode":
        low = 1
        high = 1000001
        lives = 1
        time = 30

    number = r.randint(low,high)
    guess = 1
    number_sb.config(from_=low, to=high-1)
    game_values = [lives, low, high, number, guess, time]
    print(game_values)

    label_update()
    # setup lives
    life_update()

    return lives, low, high, number, guess, time

def load_sounds():
    global sfx_list
    paths = ["assets/sounds/Buzzer.wav",
             "assets/sounds/Click.mp3",
             "assets/sounds/Correct.wav",
             "assets/sounds/Fail.mp3"]
    # win 2
    # click 1
    # buzzer 0
    # lose 3
    for name in paths:
        sfx_list.append(pg.mixer.Sound(name))
    pg.mixer.music.load("assets/sounds/Bg Music.mp3")

def countdown():
    global game_values
    game_values[-1] -= 1
    if game_values[-1] < 0:
        game_over()
        return
    label_update()
    root.after(1000, countdown)

def load_data(path):
    data = []
    try:
        file = open(path, "r")
        data = file.readlines()
        file.close()
    except:
        messagebox.showerror("Error", "Could not deal with your stupidity")
        root.destroy()

    temp = []
    for i in data:
        x = i.lower().capitalize().strip("\n")
        temp.append(x)
    data = temp
    print(data)

    return data

def main():
    global root
    global game_values
    global low_list
    global high_list
    global lose_list
    pg.mixer.init()
    load_sounds()
    pg.mixer.music.play(-1)
    root = root_setup()
    create_widgets(root)
    low_list = load_data("assets/text_documents/low")
    high_list = load_data("assets/text_documents/high")
    lose_list = load_data("assets/text_documents/loser")
    lives, low, high, number, guess, time = setup_game("")
    game_values = [lives, low, high, number, guess, time]
    root.after(1000, countdown)

    root.mainloop()

main()