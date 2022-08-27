from stdiomask import getpass
from cryptography.fernet import Fernet
import os
import os.path
import time

clear = lambda: os.system("cls")

keyFileExists = os.path.exists("mykey.key")
if keyFileExists == False:
    with open("mykey.key", "wb") as keyfile:
        keyfile.write(Fernet.generate_key())
        keyfile.close()
with open('mykey.key', "rb") as mykey:
    key = mykey.read()
f = Fernet(key)

def bigTitle():
    print("""            _____     __  ___                     ___ ___   ___         
 ________  / ___/__  / /_/ _ \___ ____ ___   _  _<  // _ \ <  / ________
/___/___/ / (_ / _ \/ __/ ___/ _ `(_-<(_-<  | |/ / // // / / / /___/___/
          \___/\___/\__/_/   \_,_/___/___/  |___/_(_)___(_)_/           
                                                                        """)

def main():
    infoFileExists = os.path.exists("userinfo.txt")
    if infoFileExists == False:
        with open("userinfo.txt", "w") as file:
            file.close()
    while True:
        clear()
        bigTitle()
        print("MAIN MENU")
        print("=========\n")
        print("home - THIS PAGE")
        print("reg - REGISTER")
        print("log - LOGIN")
        print("exit - EXIT TO DESKTOP\n\n")
        userChoice = input(">$")
        if userChoice in ['reg' , 'log', 'exit', 'ctrlcpugzadmin']:
            break
    if userChoice == "reg":
        register()
    elif userChoice == "log":
        login()
    elif userChoice == "exit":
        exit()
    elif userChoice == "ctrlcpugzadmin":
        adminLogin()

def register():
    while True:
        clear()
        bigTitle()
        print("REGISTER")
        print("========\n")
        username = input("ENTER A USERNAME TO REGISTER\nNOTE: NO SPACES\n\nhome - EXIT TO MAIN MENU\n\n>>")
        if username == "home":
            main()
        elif userAlreadyExists(username):
            print("***ERR: THERE IS ANOTHER USER WITH THIS NAME")
            time.sleep(1.5)
            continue
        elif len(username) > 0:
            x = username.find(" ")
            if x == -1:
                break
            else:
                print("***ERR: USERNAMES CAN NOT CONTAIN SPACES")
                time.sleep(1.5)
                continue
        elif username != "":
            break

    while True:
        clear()
        bigTitle()
        print("REGISTER")
        print("========\n")
        userPass = getpass("ENTER A PASSWORD\nNOTE: NO SPACES\n\n>>")
        if len(userPass) > 0:
            x = userPass.find(" ")
            if x == -1:
                clear()
                bigTitle()
                print("REGISTER")
                print("========\n")
                confirmUserPass = getpass("CONFIRM PASSWORD\n\n>>")
                if userPass == confirmUserPass:
                    break
                else:
                    print("***ERR: PASSWORDS DO NOT MATCH")
                    time.sleep(1.5)
                    continue
            else:
                print("***ERR: PASSWORDS CAN NOT CONTAIN SPACES")
                time.sleep(1.5)
                continue
    addUserInfo([username, f.encrypt(bytes(userPass, 'utf-8'))])
    print("SUCCESS!")
    time.sleep(2)
    main()

def login():
    x = 3
    while True:
        clear()
        bigTitle()
        print("USERNAME LOGIN")
        print("==============\n")
        print("home - EXIT TO MAIN MENU\n\n")
        userInfo = {}
        with open("userinfo.txt", "r") as file:
            for line in file:
                line = line.split()
                userInfo.update({line[0]: line[1]})
        username = input(">>")
        if username == "home":
            main()
        elif username not in userInfo:
            print("***ERR: USER DOES NOT EXIST")
            time.sleep(1.5)
            continue
        else:
            break

    while True:
        clear()
        bigTitle()
        print("PASSWORD LOGIN")
        print("==============\n")
        userPass = getpass(">>")
        x -= 1
        if not checkPasswordHash(userPass, userInfo[username]):
            print(f"***ERR: PASSWORD INCORRECT\nNOTE: {x} TRIES REMAINING")
            time.sleep(1.5)
            if x == 0:
                print("***ERR: NO MORE RETRIES")
                time.sleep(1.5)
                main()
        else:
            print("LOGIN SUCCESSFUL!")
            time.sleep(1)
            loadingLetters(1)
            break
    loggedIn(username)   

def loggedIn(username):
    while True:
        while True:    
            clear()
            bigTitle()
            intro = (f"WELCOME, {username}!")
            print(intro)
            length = len(intro)
            print("=" * length + "\n")
            print("loghome - THIS PAGE")
            print("new - NEW FILE")
            print("edit - EDIT FILE")
            print("view - VIEW FILE")
            print("del - DELETE FILE")
            print("home - LOGOUT")
            userInput = input("exit - LOGOUT AND QUIT TO DESKTOP\n\n>%")
            if userInput in ["new", "edit", "view", "home", "exit", "del"]:
                break
            else:
                continue
        if userInput == "edit":
            editFileExists = os.path.exists(f"{username}.txt")
            if editFileExists == False:
                print("***ERR: FILE DOES NOT EXIST!")
                time.sleep(1.5)
                continue
            else:
                editDoc(username)
        elif userInput == "view":
            viewFileExists = os.path.exists(f"{username}.txt")
            if viewFileExists == False:
                print("***ERR: FILE DOES NOT EXIST!")
                time.sleep(1.5)
                continue
            else:
                viewDoc(username)
        elif userInput == "del":
            delFileExists = os.path.exists(f"{username}.txt")
            if delFileExists == False:
                print("***ERR: FILE DOES NOT EXIST!")
                time.sleep(1.5)
                continue
            else:
                delDoc(username)
        else:
            break
    if userInput == "home":
        main()
    elif userInput == "exit":
        exit()
    elif userInput == "new":
        newDoc(username)

def adminLogin():
    x = 3
    while True:
        clear()
        bigTitle()
        print("ADMIN LOGIN")
        print("===========\n")
        print("home - EXIT TO MAIN MENU\n\n")
        userInfo = {}
        with open("userinfo.txt", "r") as file:
            for line in file:
                line = line.split()
                userInfo.update({line[0]: line[1]})
        username = input(">>")
        if username == "home":
            main()
        elif username not in userInfo:
            print("***ERR: USER DOES NOT EXIST")
            time.sleep(1.5)
            continue
        else:
            break

    while True:
        clear()
        bigTitle()
        print("PASSWORD LOGIN")
        print("==============\n")
        userPass = getpass(">>")
        x -= 1
        if not checkPasswordHash(userPass, userInfo[username]):
            print(f"***ERR: PASSWORD INCORRECT\nNOTE: {x} TRIES REMAINING")
            time.sleep(1.5)
            if x == 0:
                print("***ERR: NO MORE RETRIES")
                time.sleep(1.5)
                main()
        else:
            print("LOGIN SUCCESSFUL!")
            time.sleep(1)
            loadingLetters(1)
            break
    adminLoggedIn(username) 

def adminLoggedIn(username):
    clear()
    bigTitle()
    intro = (f"WELCOME, {username}!")
    print(intro)
    length = len(intro)
    print("=" * length + "\n")
    input()

#SMALL DEFINITIONS
#SMALL DEFINITIONS
#SMALL DEFINITIONS

def viewDoc(username):
    while True:
        clear()
        bigTitle()
        print("VIEW FILE | NOTE: LISTED AS [ACCOUNT, USERNAME, PASSWORD]")
        print("=========   =============================================\n")
        print("LINE# | INFO\n")
        with open(username + ".txt", "rb") as file:
            lines = file.readlines()
        count = 0
        for line in lines:
            sline = line.split(b' ')
            if count != 0:
                print("==========")
            for i in range(3):
                count += 1
                newString = sline[i]
                decrypt = f.decrypt(newString)
                decode = decrypt.decode('utf-8')
                print(f"LINE {count}: {decode}")
        if count != 0:
            userInput = input("\nSUCCESS!\nTYPE 'home' TO EXIT\n\n>>")
        else:
            userInput = input("\nNO DATA SAVED!\nTYPE 'home' TO EXIT\n\n>>")
        if userInput in ["home"]:
            break
    loggedIn(username)

def editDoc(username):
    while True:
        clear()
        bigTitle()
        print("EDIT FILE")
        print("=========\n")
        userInput = input("ARE YOU SURE YOU WANT TO WRITE TO FILE? (Y/N TO CONFIRM)\n\n>>")
        if userInput in ["y", "n"]:
            break
    if userInput == "n":
        print("FILE WRITEUP CANCELED\n\n")
        time.sleep(1.5)
        loggedIn(username)
    elif userInput == "y":
        while userInput == "y":    
            while True:
                for i in range(3):
                    clear()
                    bigTitle()
                    print("WRITING FILE")
                    print("============\n")
                    write = {0: "ACCOUNT", 1: "USERNAME", 2: "PASSWORD"}
                    if i <= 1:
                        userInput = input(f"WRITE: {str(write[i])}\n\n>>")
                    else:
                        userInput = getpass(f"WRITE: {str(write[i])}\n\n>>")
                    encrypted = f.encrypt(bytes(userInput, 'utf-8'))
                    with open(f"{username}.txt", "ab") as file:
                        file.write(encrypted)
                        file.write(b' ')
                        if i == 2:
                            file.write(b'\n')
                userInput = input("CONTINUE WRITING? (Y/N TO CONFIRM)\n\n>>")
                if userInput in ["y", "n"]:
                    break
            if userInput == "y":
                continue
            else:
                print("SUCCESS!\n\n")
                time.sleep(1.5)
                loggedIn(username)                    

def newDoc(username):
    while True:    
        clear()
        bigTitle()
        print("NEW FILE")
        print("========\n")
        userInput = input("ARE YOU SURE YOU WANT TO MAKE A NEW FILE?\nNOTE: THIS WILL PERMANATELY DESTROY AN OLD FILE (Y/N TO CONFIRM)\n\n>>").lower()
        if userInput in ["y", "n"]:
            break
    if userInput == "n":
        print("FILE CREATION CANCELED")
        time.sleep(1.5)
        loggedIn(username)
    else:
        with open(f"{username}.txt", "w") as file:
            print("SUCCESS!\n\n")
            time.sleep(1.5)
            loggedIn(username)

def delDoc(username):
    while True:
        clear()
        bigTitle()
        print("DELETE FILE")
        print("===========\n")
        userInput = input("ARE YOU SURE YOU WANT TO DELETE YOUR FILE?\nNOTE: THIS WILL DESTROY YOUR FILE AND CAN NOT BE UNDONE! (Y/N TO CONFIRM)\n\n>>").lower()
        if userInput in ["y", "n"]:
            break
        else:
            print("***ERR: INVALID COMMAND!")
            time.sleep(1.5)
            continue
    if userInput == "n":
        print("CANCELED!\n\n")
        time.sleep(1.5)
        loggedIn(username)
    else:
        os.remove(f"{username}.txt")
        print("SUCCESS!\n\n")
        time.sleep(1.5)
        loggedIn(username)

def userAlreadyExists(username):
    with open("userinfo.txt", "r") as file:
        for line in file:
            line = line.split()
            if line[0] == username:
                return True
        return False

def addUserInfo(userInfo: list):
    with open("userinfo.txt", "ab") as file:
        for info in userInfo:
            if info == userInfo[0]:
                file.write(bytes(info, encoding="utf-8"))
            else:
                file.write(info)
            file.write(b" ")
        file.write(b"\n")

def loadingScreen(x):
    clear()
    bigTitle()
    time.sleep(0.5)
    loadingLetters(x)

def checkPasswordHash(password, hash):
    decrypt = f.decrypt(bytes(hash, encoding="utf-8"))
    decode = decrypt.decode('utf-8')
    return password == decode

def loadingLetters(x): 
    for i in range(x):
        print("LOADING (*-----)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (-*----)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (--*---)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (---*--)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (----*-)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (-----*)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (----*-)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (---*--)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (--*---)")
        time.sleep(0.02)
        clear()
        bigTitle()
        print("LOADING (-*----)")
        time.sleep(0.02)
        clear()
        bigTitle()


loadingScreen(2)
main()