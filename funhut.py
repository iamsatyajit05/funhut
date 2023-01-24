
#import modules
 
from tkinter import *
import tkinter
import database
import game1_tetris
import game2_snake
import game3_fourrowking
 
def config():
    config.current_screen = ''

config()

# Designing window for registration
 
def register():
    if config.current_screen=='login':
        login_screen.destroy()
    config.current_screen = 'register'
    # elif call=='home'

    global register_screen
    # register_screen = Toplevel(main_screen)
    register_screen = Tk()
    register_screen.title("Register | FunHut")

    screen_width = register_screen.winfo_screenwidth()
    screen_height = register_screen.winfo_screenheight()
    top_margin = (screen_height - screen_height/2)/2 - 50
    left_margin = (screen_width - screen_width/4)/2
    register_screen.geometry("%dx%d+%d+%d" % (screen_width/4, screen_height/2, left_margin, top_margin))
    register_screen.resizable(False,False)
    global username
    global password
    global email
    global username_entry
    global password_entry
    global email_entry
    global errorregister_signup
    username = StringVar()
    password = StringVar()
    email = StringVar()
 
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(register_screen, text="Register", justify='center', width="30", font=("calibri", 14)).pack()
    Label(text="").pack()
    username_lable = Label(register_screen, text="Username", anchor='w', width=18)
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username, width=20)
    username_entry.pack()
    email_lable = Label(register_screen, text="Email", anchor='w', width=18)
    email_lable.pack()
    email_entry = Entry(register_screen, textvariable=email, width=20)
    email_entry.pack() 
    password_lable = Label(register_screen, text="Password", anchor='w', width=18)
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*', width=20)
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, command = register_user).pack()
    Button(register_screen,text="Existing User? Login", height="1", width="20", bd="0", font= "Arial 8 underline", command=login).pack()
    errorregister_signup = Label(register_screen, text='', fg="red", font=("calibri", 11))
    errorregister_signup.pack()
 
 
# Designing window for login 
 
def login():
    if config.current_screen == 'home':
        main_screen.destroy()

    elif config.current_screen == 'register':
        register_screen.destroy()

    elif config.current_screen == 'game':
        game_scrren.destroy()

    else:
        pass
    config.current_screen = 'login'

    global login_screen
    # login_screen = Toplevel(main_screen)
    login_screen = Tk()
    login_screen.title("Login | FunHut")

    screen_width = login_screen.winfo_screenwidth()
    screen_height = login_screen.winfo_screenheight()
    top_margin = (screen_height - screen_height/2)/2 - 50
    left_margin = (screen_width - screen_width/4)/2
    login_screen.geometry("%dx%d+%d+%d" % (screen_width/4, screen_height/2, left_margin, top_margin))
    login_screen.resizable(False,False)
    # Label(login_screen, text="Start fun by Sign-In", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
    global errorregister_login
 
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(login_screen, text="Log In", justify='center', width="30", font=("calibri", 14)).pack()
    Label(text="").pack()
    Label(login_screen, text="Username", anchor='w', width=18).pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify, width=20)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password", anchor='w', width=18).pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*', width=20)
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
    Button(login_screen,text="New User? Register", height="1", width="20", bd="0", font= "Arial 8 underline", command=register).pack()
    errorregister_login = Label(login_screen, text='', fg="red", font=("calibri", 11))
    errorregister_login.pack()

 
def register_user():
 
    username_info = username.get()
    email_info = email.get()
    password_info = password.get()
 
    account_create_response = database.register_user(username_info, email_info, password_info)
 
    if account_create_response == 'Account created successfully!!':
        # Label(register_screen, text=account_create_response, fg="green", font=("calibri", 11)).pack()
        errorregister_signup['text'] = account_create_response
        errorregister_signup['fg'] = "green"
        login()
    
    elif account_create_response == 'User already exist!!':
        username_entry.delete(0, END)
        errorregister_signup['text'] = account_create_response
        errorregister_signup['fg'] = "red"

    elif account_create_response == 'No field can be empty!!':
        username_entry.delete(0, END)
        errorregister_signup['text'] = account_create_response
        errorregister_signup['fg'] = "red"
    
    elif account_create_response == 'Email not valid!!':
        email_entry.delete(0, END)
        errorregister_signup['text'] = account_create_response
        errorregister_signup['fg'] = "red"

    else:
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        errorregister_signup['text'] = account_create_response
        errorregister_signup['fg'] = "red"
 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    login_create_response = database.login_user(username1, password1)
    
    if login_create_response == 'Login Successfull!!':
        errorregister_login['text'] = login_create_response
        errorregister_login['fg'] = "green"
        game_home_scrren()

    elif login_create_response == 'Invalid Password!!':
        errorregister_login['text'] = login_create_response
        errorregister_login['fg'] = "red"
        
    elif login_create_response == 'User not found!!':
        errorregister_login['text'] = login_create_response
        errorregister_login['fg'] = "red"

    else:
        errorregister_login['text'] = login_create_response
        errorregister_login['fg'] = "red"

def game_home_scrren():
    if config.current_screen == 'login':
        login_screen.destroy()
    elif config.current_screen == 'home':
        main_screen.destroy()

    config.current_screen = 'game'
    global game_scrren
    # login_screen = Toplevel(main_screen)
    game_scrren = Tk()
    game_scrren.title("Playzone | FunHut")

    screen_width = game_scrren.winfo_screenwidth()
    screen_height = game_scrren.winfo_screenheight()
    top_margin = (screen_height - screen_height/2)/2 - 50
    left_margin = (screen_width - screen_width/4)/2
    game_scrren.geometry("%dx%d+%d+%d" % (screen_width/4, screen_height/2, left_margin, top_margin))
    game_scrren.resizable(False,False)
    Button(game_scrren,text="Back", anchor='w', height="1", width="50", bd="0", font= "Arial 8", command=main).pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(game_scrren, text="Single Player", justify='center', width="30", font=("calibri", 14)).pack()
    Button(text="Tetris", height="2", width="30", command=game1_tetris.rungame).pack()
    Label(text="").pack()
    Button(text="Snake Eat", height="2", width="30", command=game2_snake.rungame).pack()
    Label(text="").pack()
    Label(game_scrren, text="Multi Player", justify='center', width="30", font=("calibri", 14)).pack()
    Button(text="Four Row King", height="2", width="30", command=game3_fourrowking.rungame).pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Button(game_scrren,text="Logout", anchor='w', height="1", width="50", bd="0", font= "Arial 8", command=login).pack()
 
def leaderboard():
    config.current_screen = 'leaderboard'
    main_screen.destroy()
    global leaderboard_screen
    # login_screen = Toplevel(main_screen)
    leaderboard_screen = Tk()
    leaderboard_screen.title("Leaderboard | FunHut")
    screen_width = leaderboard_screen.winfo_screenwidth()
    screen_height = leaderboard_screen.winfo_screenheight()
    top_margin = (screen_height - screen_height/2)/2 - 50
    left_margin = (screen_width - screen_width/4)/2
    leaderboard_screen.geometry("%dx%d+%d+%d" % (screen_width/4, screen_height/2, left_margin, top_margin))
    leaderboard_screen.resizable(False,False)
    leaderboarddata = database.get_leaderboard()
    Button(leaderboard_screen,text="Back", anchor='w', height="1", width="50", bd="0", font= "Arial 8", command=main).pack()
    Label(text="").pack()
    Label(leaderboard_screen, text="Tetris", justify='center', width="30", font=("calibri", 14)).pack()
    user_leaderboarddata = leaderboarddata[0]
    for i, j in user_leaderboarddata.items():
        Label(leaderboard_screen, text=f'{i}: {j}', justify='center', width="30").pack()
    
    Label(text="").pack()
    Label(leaderboard_screen, text="Snake Eat", justify='center', width="30", font=("calibri", 14)).pack()
    user_leaderboarddata = leaderboarddata[1]
    for i, j in user_leaderboarddata.items():
        Label(leaderboard_screen, text=f'{i}: {j}', justify='center', width="30").pack()   
 
def main():
    if config.current_screen=='leaderboard':
        leaderboard_screen.destroy()
    if config.current_screen=='game':
        game_scrren.destroy()
        
    config.current_screen='home'

    global main_screen
    main_screen = Tk()
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    top_margin = (screen_height - screen_height/2)/2 - 50
    left_margin = (screen_width - screen_width/4)/2
    main_screen.geometry("%dx%d+%d+%d" % (screen_width/4, screen_height/2, left_margin, top_margin))
    main_screen.resizable(False, False)
    main_screen.title("Welcome to FunHut")
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="FunHut", font=("calibri", 30)).pack()
    Label(text="Your last stope for fun :)").pack()
    Label(text="").pack()
    Button(text="Play Game", height="2", width="30", command=game_home_scrren).pack()
    Label(text="").pack()
    Button(text="Leaderboard", height="2", width="30", command=leaderboard).pack()

    if not database.last_login():
        login()

    main_screen.mainloop()
 
main()