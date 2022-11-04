import requests
# necessary imports
import secrets
import string

def password_generator():


    # define the alphabet
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    alphabet = letters + digits + special_chars

    # fix password length
    pwd_length = 12

    # generate a password string
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))

    return pwd

class Person:
    def __init__(self):
        res = self.get_person_data()
        self.name = res['name']
        self.email_u = res['email_u']
        self.username = res['username']
        self.password = password_generator()

    def get_person_data(self):
        api_url = "https://api.namefake.com/ukrainian-ukraine/"
        res = requests.get(api_url).json()
        return res

    def __str__(self):
        return f"Name: {self.name}\n"\
               f"Email: {self.email_u}\n"\
               f"Username: {self.username}\n"\
               f"Password: {self.password}\n"


if __name__ == '__main__':
    p = Person()
    print(p)

    # password_generator()