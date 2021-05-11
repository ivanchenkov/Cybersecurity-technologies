import re
import pickle

attempts = 0

login_dictionary = {
    "admin": "admin",
}

block_array = []
login_attempts = {}


def system_close():  # сохранение и выход с программы
    data_saving()
    exit()


def data_saving():  # соханяем данные юзеров и их статус в файлы
    login_pickle = open('Login.pkl', 'wb')
    block_pickle = open('BlocUser.pkl', 'wb')
    pickle.dump(login_dictionary, login_pickle)
    pickle.dump(block_array, block_pickle)
    login_pickle.close()
    block_pickle.close()


def data_loading():  # выгрузка данных
    login_dictionary_file = open('Login.pkl.pkl', 'rb')
    block_pickle_file = open("BlocUser.pkl", 'rb')
    global login_dictionary
    global block_array
    login_dictionary = pickle.load(login_dictionary_file)
    block_array = pickle.load(block_pickle_file)
    login_dictionary_file.close()
    block_pickle_file.close()


def password_change(login):     # смена пароля
    correct = False
    usage_text = input("Old password: ")
    if login_dictionary[login] != usage_text:
        while not correct:
            print("Password is invalid")
            usage_text = input("Old password: ")
            if login_dictionary[login] == usage_text:
                correct = True
    usage_text = input("New password: ")
    while not check_passwd(usage_text):
        print("incorrect password")
        usage_text = input("New password: ")
    login_dictionary[login] = usage_text
    print("Password has been set")


def check_passwd(passwd):   # реглуярка для пароля!
    if re.findall(r'^.*(?=.*[a-zA-Z]+)(?=.*[,.!?`]+)', passwd):
        return True
    else:
        return False


def user_check(login):  # проверка данных
    if login in login_dictionary:
        return True


def login_in_system():  # авторизация
    global attempts
    login = input("Login: ")
    passwd = input("Password: ")
    try:
        if login_dictionary[login]:
            pass
    except KeyError:
        print("Wrong credentials")
        login_in_system()
    if login in block_array:
        print("Account in block")
        login_in_system()
    if login_dictionary[login] != passwd:
        if login not in login_attempts.keys():
            login_attempts[login] = 0
        login_attempts[login] += 1
        print("Wrong password" + "\n" + str(3 - login_attempts[login]) + " attempts left")
        if login_attempts[login] == 3:
            system_close()
        login_in_system()
    else:
        menu_choose(login)


def menu_for_user(login):   # меню
    print("Hello," + login)
    usage_text = int(input("""
1. Change password
2. Login Menu
3. Info
4. Exit from system
Please select: """))
    if usage_text == 1:
        password_change(login)
        menu_for_user(login)
    if usage_text == 2:
        login_in_system()
    if usage_text == 3:
        print("Ivanchenkov M, FB-84, var-11 ")
    if usage_text == 4:
        system_close()
    else:
        print("Wrong paragraph chosen, please enter another")
        menu_for_user(login)


def menu_for_admin():
    print("Aadmin:")
    usage_text = int(input("""
1. User list
2. Change password
3. login
4. Info
5. Exit
Select: """))
    if usage_text == 1:
        user_list = []
        blocked_user_list = []
        for key, value in login_dictionary.items():
            user_list.append(key)
        for login in block_array:
            blocked_user_list.append(login)
        usage_text = int(input("Users:" + str(user_list) + "\n" + "Blocked users: "
                               + str(blocked_user_list)
                               + """
1. Add User
2. Block/Unblock User
3. Menu
Select:"""))
        if usage_text == 1:
            usage_text = input("Name of new user: ")
            if usage_text == "" or user_check(usage_text):
                print("User already exists, please type another name: ")
                menu_for_admin()
            login_dictionary[usage_text] = ""
            print("User " + usage_text + " was added\n")
            menu_for_admin()
        if usage_text == 2:
            usage_text = input("Write user to block/unblock: ")
            if not user_check(usage_text):
                menu_for_admin()
            if usage_text in block_array:
                block_array.remove(usage_text)
                print(usage_text, "successfully unblocked")
            else:
                block_array.append(usage_text)
                print(usage_text, "successfully blocked")
                menu_for_admin()
        if usage_text == 3:
            menu_for_admin()
        else:
            print("Wrong paragraph chosen, please enter another")
            menu_for_admin()
    if usage_text == 2:
        password_change("admin")
        menu_for_admin()
    if usage_text == 3:
        login_in_system()
    if usage_text == 4:
        print("Ivanchenkov M, FB-84, var-11 ")
    if usage_text == 5:
        system_close()


def menu_choose(login):
    if login == "admin":
        menu_for_admin()
    else:
        menu_for_user(login)


if __name__ == "__main__":
    try:
        data_loading()
    except:
        pass
    login_in_system()
