import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import date, datetime

scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] 

#credentials to the account
cred = ServiceAccountCredentials.from_json_keyfile_name('config.json',scope_app) 

# authorize the clientsheet 
client = gspread.authorize(cred)

# get the sample of the Spreadsheet
sheet = client.open('FunHut')

# get the first sheet of the Spreadsheet
userdata = sheet.get_worksheet(0)
leaderboarddata = sheet.get_worksheet(1)

# records = userdata.get_all_records()

def register_user(name, email, password):
    emailvalidation = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    userid = userdata.col_values(1)
    userid = int(userid[len(userid)-1]) + 1
    alreadyusername = userdata.col_values(2)
    print(name.strip())
    if not name.strip() or not password.strip():
        return 'No field can be empty!!'
    
    elif not re.fullmatch(emailvalidation, email):
        return 'Email not valid!!'

    if name in alreadyusername:
        return 'User already exist!!'
    else:
        userdata.append_row([userid, name, email, password])
        leaderboarddata.append_row([userid, 0, 0])
        return 'Account created successfully!!'

def login_user(name, password):
    alreadyusername = userdata.col_values(2)
    alreadypassword = userdata.col_values(4)

    if name in alreadyusername:
        # print(alreadypassword[alreadyusername.index(name)], password)
        if alreadypassword[alreadyusername.index(name)] == password:
            localtime_file = open('localtime_file.txt', 'w')
            localtime_file.writelines([f"{name}\n", str(datetime.now().strftime("%Y-%m-%d"))])
            localtime_file.close()
            alreadyusername = userdata.col_values(2)
            userdata.update_cell(alreadyusername.index(name)+1, 5, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 'Login Successfull!!'
        else:
            return 'Invalid Password!!'
    
    else:
        return 'User not found!!'

def get_leaderboard():
    alreadyusername = userdata.col_values(2)
    user_userids = userdata.col_values(1)
    game_userids = leaderboarddata.col_values(1)
    original_game1 = leaderboarddata.col_values(2)
    original_game2 = leaderboarddata.col_values(3)
    # print(original_game1, original_game2)
    game1 = original_game1[1:]
    game2 = original_game2[1:]
    game1 = [int(x) for x in game1]
    game2 = [int(x) for x in game2]
    game1.sort()
    game1.reverse()
    game2.sort()
    game2.reverse()
    game1 = game1[:5]
    game2 = game2[:5]
    # print(game1, game2)

    returngame1 = {}
    for i in range(5):
        userid = game_userids[original_game1.index(str(game1[i]))]
        username = alreadyusername[user_userids.index(userid)]
        returngame1[username] = game1[i]
    
    returngame2 = {}
    for i in range(5):
        userid = game_userids[original_game2.index(str(game2[i]))]
        username = alreadyusername[user_userids.index(userid)]
        returngame2[username] = game2[i]

    localtime_file = open('localtime_file.txt', 'r')
    data = localtime_file.readlines()
    user = data[0]
    user = user[:-1]
    localtime_file.close()
    alreadyusername = userdata.col_values(2)
    userids = userdata.col_values(1)

    userid = userids[alreadyusername.index(user)]
    userids = leaderboarddata.col_values(1)
    userid = userids.index(userid)
    returngame1['You'] = original_game1[game_userids.index(str(userid))]
    returngame2['You'] = original_game2[game_userids.index(str(userid))]
    # print(returngame1, returngame2)
    return [returngame1, returngame2]


def set_leaderboard(game, score):
    localtime_file = open('localtime_file.txt', 'r')
    data = localtime_file.readlines()
    user = data[0]
    user = user[:-1]
    localtime_file.close()

    alreadyusername = userdata.col_values(2)
    userids = userdata.col_values(1)

    userid = userids[alreadyusername.index(user)]
    userids = leaderboarddata.col_values(1)
    userid = userids.index(userid)
    game = 2 if game == 'tetris' else 3
    if int(score) > int(leaderboarddata.cell(userid+1, game).value):
        leaderboarddata.update_cell(userid+1, game, score)

def last_login():
    localtime_file = open('localtime_file.txt', 'r')
    data = localtime_file.readlines()
    time = data[1]
    localtime_file.close()
    time_difference  = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S") - datetime.strptime(time, "%Y-%m-%d")
    if time_difference.days < 7:
        return True
    else:
        return False