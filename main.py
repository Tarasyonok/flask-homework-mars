from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/database.db")

    data = [
        {"surname": "Scott", "name": "Ridley", "age": 21, "position": "captain", "speciality": "research engineer", "address": "module_1", "email": "scott_chief@mars.org"},
        {"surname": "Kirillov", "name": "Dmitry", "age": 38, "position": "member", "speciality": "teacher", "address": "бул. Космонавтов, 9, Красногорск", "email": "kirillov@yandexlyceum.ru"},
        {"surname": "Mask", "name": "Elon", "age": 52, "position": "owner", "speciality": "investor", "address": "Rocket Road, Hawthorne California, CA 90250, USA", "email": "info@spacex.com"},
        {"surname": "Gagarin", "name": "Yuri", "age": 90, "position": "member", "speciality": "pilot", "address": "Ленинский просп., 39Б, Москва", "email": "yuri_gagarin@mars.org"},
    ]

    db_sess = db_session.create_session()

    for person in data:
        print(person)
        user = User()
        user.surname = person["surname"]
        user.name = person["name"]
        user.age = person["age"]
        user.position = person["position"]
        user.speciality = person["speciality"]
        user.address = person["address"]
        user.email = person["email"]
        db_sess.add(user)
        db_sess.commit()


if __name__ == 'main':
    main()
