import time

import requests
# necessary imports
import secrets
import string
import random


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
        # self.email_u = res['email_u']
        self.email_u = self.generate_email()
        self.username = res['username']
        self.password = password_generator()

    def get_person_data(self):
        api_url_namefake = "https://api.namefake.com/ukrainian-ukraine/"
        api_url_reserv = "https://random-data-api.com/api/v2/users"
        try:
            res = requests.get(api_url_namefake).json()
            self.name = res['name']
            return res
        except requests.exceptions.ConnectionError:
            print("Use reserv api")
            res = requests.get(api_url_reserv).json()
            print(res)
            result = {}
            result.update({"name": res["first_name"],
                           "last_name": res["last_name"],
                           "email_u": res["email"].split("@")[0],
                           "username": res["username"],
                           "height": random.randint(150,200),
                           "blood": random.randint(0,3),
                           "weight": random.randint(50, 120)})
            return result

    def generate_email(self):
        parameters_nums = ['height', 'weight', 'blood']
        parameters_str = ['email_u', 'username']  # 'eye', 'sport'
        result = ""
        data = self.get_person_data()
        result += str(data[random.choice(parameters_str)]) + random.choice(["", "_", "-", "."]) + str(
            data[random.choice(parameters_nums)])
        return result[0:-1].replace(" ", "")

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Email: {self.email_u}\n" \
               f"Username: {self.username}\n" \
               f"Password: {self.password}\n"


if __name__ == '__main__':
    for i in range(50):
        try:
            print(f"---------------{i}---------------")
            p = Person()
            print(p)
        except Exception as e:
            print(f"Exception: {e}")
            break
        time.sleep(2)
    # print(p.get_person_data())
    # print(p.generate_email())


    # password_generator()
