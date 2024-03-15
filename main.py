import datetime

import flask
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from forms.user import RegisterForm, LoginForm
from forms.jobs import AddJobForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/database.db")
    # add_users()
    # show_users()
    # add_departments()
    app.run()


def show_users():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user.surname, user.name)


# def add_jobs():
#     data = [
#         {"team_leader": 1, "job": "deployment of residential modules 1 and 2",
#          "work_size": 15, "collaborators": "2, 3",
#          "is_finished": False},
#     ]
#
#     db_sess = db_session.create_session()
#
#     for info in data:
#         print(info)
#         job = Jobs()
#         job.team_leader = info["team_leader"]
#         job.job = info["job"]
#         job.work_size = info["work_size"]
#         job.collaborators = info["collaborators"]
#         job.is_finished = info["is_finished"]
#         db_sess.add(job)
#         db_sess.commit()
#
def add_users():
    data = [
        {"surname": "a", "name": "b", "age": 1, "position": "tester", "speciality": "tester",
         "address": "module_1", "email": "a@b", "password": "123"},
        {"surname": "Scott", "name": "Ridley", "age": 21, "position": "captain", "speciality": "research engineer",
         "address": "module_1", "email": "scott_chief@mars.org", "password": "123"},
        {"surname": "Kirillov", "name": "Dmitry", "age": 38, "position": "member", "speciality": "teacher",
         "address": "бул. Космонавтов, 9, Красногорск", "email": "kirillov@yandexlyceum.ru", "password": "123"},
        {"surname": "Mask", "name": "Elon", "age": 52, "position": "owner", "speciality": "investor",
         "address": "Rocket Road, Hawthorne California, CA 90250, USA", "email": "info@spacex.com", "password": "123"},
        {"surname": "Gagarin", "name": "Yuri", "age": 90, "position": "member", "speciality": "pilot",
         "address": "Ленинский просп., 39Б, Москва", "email": "yuri_gagarin@mars.org", "password": "123"},
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
        user.set_password(info["password"])
        db_sess.add(user)
        db_sess.commit()
#
# def add_departments():
#     data = [
#         {"title": "battling the forces of Hell, consisting of demons and the undead", "chief": 1,
#          "email": "doom@mars.com", "members": "1, 4"},
#     ]
#
#     db_sess = db_session.create_session()
#
#     for info in data:
#         department = Department()
#         department.title = info["title"]
#         department.chief = info["chief"]
#         department.email = info["email"]
#         department.members = info["members"]
#         db_sess.add(department)
#         db_sess.commit()
#         print(department)


@app.route("/")
def index():
    db_sess = db_session.create_session()

    param = {}
    param["activities"] = db_sess.query(Jobs).all()
    param["leaders"] = []
    for job in param["activities"]:
        leader = db_sess.query(User).get(job.team_leader)
        param["leaders"].append(f"{leader.name} {leader.surname}")
    param["current_user"] = current_user
    return flask.render_template('job-journal.html', **param)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return flask.render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return flask.render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return flask.redirect('/login')
    return flask.render_template('register.html', title='Регистрация', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")
        return flask.render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return flask.render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect("/")


@app.route('/addjob',  methods=['GET', 'POST'])
@login_required
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        local_user = db_sess.merge(current_user)
        job.creator = local_user
        # local_object = db_session.merge(original_object)
        db_sess.add(job)
        db_sess.commit()
        return flask.redirect('/')
    return flask.render_template('addjob.html', title='работы',
                           form=form)


@app.route('/editjob/<int:job_id>', methods=['GET', 'POST'])
@login_required
def editjob(job_id):
    form = AddJobForm()
    if flask.request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            flask.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Jobs).get(job_id)
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id,
                                              Jobs.creator == current_user,
                                              ).first()
        if job:
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return flask.redirect('/')
        else:
            flask.abort(404)
    return flask.render_template('addjob.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/deletejob/<int:job_id>', methods=['GET', 'POST'])
@login_required
def deletejob(job_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        job = db_sess.query(Jobs).get(job_id)
    else:
        job = db_sess.query(Jobs).filter(Jobs.id == job_id,
                                         Jobs.creator == current_user,
                                         ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        flask.abort(404)

    return flask.redirect('/')


# @app.route("/cookie_test")
# def cookie_test():
#     visits_count = int(flask.request.cookies.get("visits_count", 0))
#     if visits_count:
#         res = make_response(
#             f"Вы пришли на эту страницу {visits_count + 1} раз")
#         res.set_cookie("visits_count", str(visits_count + 1),
#                        max_age=60 * 60 * 24 * 365 * 2)
#     else:
#         res = make_response(
#             "Вы пришли на эту страницу в первый раз за последние 2 года")
#         res.set_cookie("visits_count", '1',
#                        max_age=60 * 60 * 24 * 365 * 2)
#     return res

# @app.route("/session_test")
# def session_test():
#     visits_count = flask.session.get('visits_count', 0)
#     flask.session['visits_count'] = visits_count + 1
#     return make_response(
#         f"Вы пришли на эту страницу {visits_count + 1} раз")


if __name__ == 'main':
    main()
