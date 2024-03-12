import datetime

from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/database.db")
    # show_users()
    app.run()


def show_users():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)


def add_jobs():
    data = [
        {"team_leader": 1, "job": "deployment of residential modules 1 and 2",
         "work_size": 15, "collaborators": "2, 3",
         "is_finished": False},
    ]

    db_sess = db_session.create_session()

    for info in data:
        print(info)
        job = Jobs()
        job.team_leader = info["team_leader"]
        job.job = info["job"]
        job.work_size = info["work_size"]
        job.collaborators = info["collaborators"]
        job.is_finished = info["is_finished"]
        db_sess.add(job)
        db_sess.commit()


def add_users():
    data = [
        {"surname": "Scott", "name": "Ridley", "age": 21, "position": "captain", "speciality": "research engineer",
         "address": "module_1", "email": "scott_chief@mars.org"},
        {"surname": "Kirillov", "name": "Dmitry", "age": 38, "position": "member", "speciality": "teacher",
         "address": "бул. Космонавтов, 9, Красногорск", "email": "kirillov@yandexlyceum.ru"},
        {"surname": "Mask", "name": "Elon", "age": 52, "position": "owner", "speciality": "investor",
         "address": "Rocket Road, Hawthorne California, CA 90250, USA", "email": "info@spacex.com"},
        {"surname": "Gagarin", "name": "Yuri", "age": 90, "position": "member", "speciality": "pilot",
         "address": "Ленинский просп., 39Б, Москва", "email": "yuri_gagarin@mars.org"},
    ]

    db_sess = db_session.create_session()

    for info in data:
        print(info)
        user = User()
        user.surname = info["surname"]
        user.name = info["name"]
        user.age = info["age"]
        user.position = info["position"]
        user.speciality = info["speciality"]
        user.address = info["address"]
        user.email = info["email"]
        db_sess.add(user)
        db_sess.commit()

@app.route("/")
def index():
    db_sess = db_session.create_session()

    param = {}
    param["activities"] = db_sess.query(Jobs).all()
    param["leaders"] = []
    for job in param["activities"]:
        leader = db_sess.query(User).get(job.team_leader)
        param["leaders"].append(f"{leader.name} {leader.surname}")
    return render_template('job-journal.html', **param)


if __name__ == 'main':
    main()
