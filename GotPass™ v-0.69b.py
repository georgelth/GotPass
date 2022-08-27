from stdiomask import getpass
import hashlib
import os
import os.path
import time
clear = lambda: os.system("cls")


def bigTitle():
    print("""            _____     __  ___                 _   __    ___   _______  __            
 ________  / ___/__  / /_/ _ \___ ____ ___   | | / /___/ _ \ / __/ _ \/ /    ________
/___/___/ / (_ / _ \/ __/ ___/ _ `(_-<(_-<   | |/ /___/ // // _ \\\\_, / _ \  /___/___/
          \___/\___/\__/_/   \_,_/___/___/   |___/    \___(_)___/___/_.__/           
                                                                                     """)

def main():
    fileExists = os.path.exists("userinfo.txt")
    if fileExists == False:
        with open("userinfo.txt", "w") as file:
            file.close()
    while True:
        clear()
        bigTitle()
        print("MAIN MENU")
        print("=========\n")
        print("reg - REGISTER")
        print("log - LOGIN")
        print("kill - EXIT TO DESKTOP\n\n")
        userChoice = input(">$")
        if userChoice in ['reg' , 'log', 'kill']:
            break
    if userChoice == "reg":
        register()
    elif userChoice == "log":
        login()
    elif userChoice == "kill":
        exit()

def register():
    while True:
        clear()
        bigTitle()
        print("REGISTER")
        print("========\n")
        username = input("ENTER A USERNAME TO REGISTER\nNOTE: NO SPACES\n\n>>")
        if userAlreadyExists(username):
            userChoice = input("***ERR: THERE IS ANOTHER USER WITH THIS NAME\n\n>$")
            mainErr(userChoice)
        elif len(username) > 0:
            x = username.find(" ")
            if x == -1:
                break
            else:
                userChoice = input("***ERR: USERNAMES CAN NOT CONTAIN SPACES\n\n>$")
                mainErr(userChoice)
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
                    userChoice = input("***ERR: PASSWORDS DO NOT MATCH\n\n>$")
                    mainErr(userChoice)
                    continue
            else:
                userChoice = input("***ERR: PASSWORDS CAN NOT CONTAIN SPACES\n\n>$")
                mainErr(userChoice)
                continue
    addUserInfo([username, hashPassword(userPass)])
    print("SUCCESS!")
    userChoice = input("\n\n>$")
    mainErr(userChoice)

def login():
    x = 3
    while True:
        clear()
        bigTitle()
        print("USERNAME LOGIN")
        print("==============\n")
        userInfo = {}
        with open("userinfo.txt", "r") as file:
            for line in file:
                line = line.split()
                userInfo.update({line[0]: line[1]})
        username = input(">>")
        if username not in userInfo:
            userInput = input("***ERR: USER DOES NOT EXIST\n\n>$")
            mainErr(userInput)
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
            print("***ERR: PASSWORD INCORRECT\nNOTE: " + str(x) + " TRIES REMAINING")
            if x == 0:
                userInput = input("***ERR: NO MORE RETRIES\n\n>$")
                mainErr(userInput)
        else:
            print("LOGIN SUCCESSFUL!")
            time.sleep(1)
            loadingLetters(2)
            break
    loggedIn(username)   

def loggedIn(username):
    while True:    
        clear()
        bigTitle()
        intro = ("WELCOME, " + username + "!")
        print(intro)
        length = len(intro)
        print("=" * length + "\n")
        print("ndoc - NEW DOCUMENT")
        print("edoc - EDIT DOCUMENT")
        print("vdoc - VIEW DOCUMENT")
        print("home - LOGOUT")
        userInput = input("kill - LOGOUT AND QUIT TO DESKTOP\n\n>%")
        if userInput in ["ndoc", "edoc", "vdoc", "home", "kill"]:
            break
        else:
            continue
    if userInput == "home":
        main()
    elif userInput == "kill":
        exit()
    elif userInput == "ndoc":
        newDoc(username)
    elif userInput == "edoc":
        editDoc(username)
    elif userInput == "vdoc":
        viewDoc(username)


#SMALL DEFINITIONS
#SMALL DEFINITIONS
#SMALL DEFINITIONS

def viewDoc(username):
    while True:
        loadingScreen(1)
        clear()
        bigTitle()
        print("VIEW DOCUMENT")
        print("=============\n")
        with open(username + ".txt", "r") as file:
            file.read()
        userInput = input("\nSUCCESS!\n\n>%")
        logErr(userInput, username)


def editDoc(username):
    while True:
        clear()
        bigTitle()
        print("EDIT DOCUMENT")
        print("=============\n")
        userInput = input("ARE YOU SURE YOU WANT TO APPEND TO FILE? (Y/N TO CONFIRM)\n\n>>")
        if userInput in ["y", "n"]:
            break
    if userInput == "n":
        userInput = input("FILE APPENDING CANCELED\n\n>%")
        logErr(userInput, username)
    elif userInput == "y":
        while userInput == "y":    
            while True:
                for i in range(3):
                    clear()
                    bigTitle()
                    print("APPENDING DOCUMENT")
                    print("==================\n")
                    write = {0: "MEMO", 1: "USERNAME", 2: "PASSWORD"}
                    userInput = input("WRITE: " + str(write[i]) + "\nfin - FINISH & SAVE\n\n>>")
                    with open(username + ".txt", "a") as file:
                        file.write(userInput)
                        file.write(" ")
                        if i == 2:
                            file.write("\n")
                userInput = input("CONTINUE APPENDING? (Y/N TO CONFIRM)\n\n>>")
                if userInput in ["y", "n"]:
                    break
            if userInput == "y":
                continue
            else:
                userInput = input("CANCELED!\n\n>%")
                logErr(userInput, username)
                break                         

def newDoc(username):
    while True:    
        clear()
        bigTitle()
        print("NEW DOCUMENT")
        print("============\n")
        userInput = input("ARE YOU SURE YOU WANT TO MAKE A NEW FILE?\nNOTE: THIS WILL PERMANATELY DESTROY AN OLD FILE (Y/N TO CONFIRM)\n\n>>").lower()
        if userInput in ["y", "n"]:
            break
    if userInput == "n":
        userInput = input("FILE CREATION CANCELED\n\n>%")
        logErr(userInput, username)
    else:
        with open(username + ".txt", "w") as file:
            userInput = input("SUCCESS!\n\n>%")
            logErr(userInput, username)

def logErr(x, username):
    while True:
        if x in ["lhome", "home", "vdoc", "kill", "edoc", "ndoc"]:
            break
        else:
            print("\nINVALID COMMAND")
            x = input("\n\n>%")
            continue
    if x == "lhome":
        loggedIn(username)
    elif x == "edoc":
        pass
    elif x == "home":
        main()
    elif x == "kill":
        exit()
    elif x == "ndoc":
        newDoc()
    elif x == "vdoc":
        pass

def mainErr(x): 
    while True:
        if x in ["reg", "log", "home", "kill"]:
            break
        else:
            print("\nINVALID COMMAND")
            x = input("\n\n>$")
            continue
    if x == "reg":
        register()
    elif x == "log":
        login()
    elif x == "home":
        main()
    elif x == "kill":
        exit()

def userAlreadyExists(username):
    with open("userinfo.txt", "r") as file:
        for line in file:
            line = line.split()
            if line[0] == username:
                return True
        return False

def addUserInfo(userInfo: list):
    with open("userinfo.txt", "a") as file:
        for info in userInfo:
            file.write(info)
            file.write(" ")
        file.write("\n")

def loadingScreen(x):
    clear()
    bigTitle()
    time.sleep(3)
    loadingLetters(x)

def hashPassword(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def checkPasswordHash(password, hash):
    return hashPassword(password) == hash

def loadingLetters(x): 
    for i in range(x):
        print("LOADING (*-------)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (-*------)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (--*-----)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (---*----)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (----*---)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (-----*--)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (------*-)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (-------*)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (------*-)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (-----*--)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (----*---)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (---*----)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (--*-----)")
        time.sleep(0.05)
        clear()
        bigTitle()
        print("LOADING (-*------)")
        time.sleep(0.05)
        clear()
        bigTitle()


loadingScreen(3)
main()