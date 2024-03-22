import datetime

import flask
from data import db_session, jobs_api, user_api
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from forms.user import RegisterForm, LoginForm
from forms.jobs import AddJobForm
from forms.department import AddDepartmentForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from requests import get, post, delete, put

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)



@app.errorhandler(400)
def bad_request(_):
    return flask.make_response(flask.jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(_):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)



def main():
    db_session.global_init("db/database.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    # add_users()
    # add_jobs()
    # add_departments()

    app.run()


def show_users():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user.surname, user.name)

def add_users():
    data = [
        {"surname": "a", "name": "b", "age": 1, "position": "tester", "speciality": "tester",
         "address": "module_1", "email": "a@b", "city_from": "Москва", "password": "123"},
        {"surname": "Scott", "name": "Ridley", "age": 21, "position": "captain", "speciality": "research engineer",
         "address": "module_1", "email": "scott_chief@mars.org", "city_from": "Санкт-Петербург", "password": "123"},
        {"surname": "Kirillov", "name": "Dmitry", "age": 38, "position": "member", "speciality": "teacher",
         "address": "бул. Космонавтов, 9, Красногорск", "email": "kirillov@yandexlyceum.ru", "city_from": "Красногорск", "password": "123"},
        {"surname": "Mask", "name": "Elon", "age": 52, "position": "owner", "speciality": "investor",
         "address": "Rocket Road, Hawthorne California, CA 90250, USA", "email": "info@spacex.com",
         "city_from": "New York", "password": "123"},
        {"surname": "Gagarin", "name": "Yuri", "age": 90, "position": "member", "speciality": "pilot",
         "address": "Ленинский просп., 39Б, Москва", "email": "yuri_gagarin@mars.org", "city_from": "Пекин", "password": "123"},
    ]

    db_sess = db_session.create_session()
    db_sess.commit()

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
        user.city_from = info["city_from"]
        user.set_password(info["password"])
        db_sess.add(user)
        db_sess.commit()


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
        job.user = db_sess.query(User).get(info["team_leader"])
        db_sess.add(job)
        job.user.jobs.append(job)
        db_sess.merge(job.user)
        db_sess.commit()


def add_departments():
    data = [
        {"title": "battling the forces of Hell, consisting of demons and the undead", "chief": 1,
         "email": "doom@mars.com", "members": "1, 4"},
    ]

    db_sess = db_session.create_session()

    for info in data:
        department = Department()
        department.title = info["title"]
        department.chief = info["chief"]
        department.email = info["email"]
        department.members = info["members"]

        department.user = db_sess.query(User).get(info["chief"])
        db_sess.add(department)
        department.user.departments.append(department)
        db_sess.merge(department.user)
        db_sess.commit()
        print(department)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    param = {}
    param["activities"] = db_sess.query(Jobs).all()
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

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return flask.redirect("/")


@app.route('/addjob/',  methods=['GET', 'POST'])
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


@app.route('/editjob/<int:job_id>/', methods=['GET', 'POST'])
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


@app.route('/deletejob/<int:job_id>/', methods=['GET', 'POST'])
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


@app.route("/users_show/<int:user_id>/")
def users_show(user_id):

    user = get(f'http://localhost:5000/api/users/{user_id}').json()["user"]
    params = {}

    params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': user['city_from'],
        'format': 'json',
    }

    geocoder_request = "http://geocode-maps.yandex.ru/1.x/"
    response = get(geocoder_request, params=params)
    print(response.url)

    if not response:
        # print("Ошибка выполнения запроса:")
        # print("Http статус:", response.status_code, "(", response.reason, ")")
        print("Нечего не нашлось")
        return flask.make_response("Нечего не нашлось")

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    try:
        bbox = json_response["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["boundedBy"]["Envelope"]
    except KeyError:
        bbox = toponym["boundedBy"]["Envelope"]
    x1, y1 = list(map(float, bbox["lowerCorner"].split(' ')))
    x2, y2 = list(map(float, bbox["upperCorner"].split(' ')))
    print(f'toponym_coodrinates: {toponym_coodrinates}')
    coods = list(map(float, toponym_coodrinates.split(' ')))

    ln = coods[0]
    lt = coods[1]

    params = {
        'll': f'{str(ln)},{str(lt)}',
        'bbox': f'{x1},{y1}~{x2},{y2}',
        'spn': f'{str(y2 - y1)},{str(y2 - y1)}',
        'l': 'sat',
        'size': '600,400',
    }

    map_request = f"http://static-maps.yandex.ru/1.x/"
    response = get(map_request, params=params)
    print(response.url)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return flask.make_response("Ошибка выполнения запроса")

    map_file = "static/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return flask.render_template('users_show.html', name=f"{user['name']} {user['surname']}")


@app.route("/departments/")
def departments():
    db_sess = db_session.create_session()
    param = {}
    param["departments"] = db_sess.query(Department).all()
    param["current_user"] = current_user
    return flask.render_template('departments.html', **param)


@app.route('/adddepartment/',  methods=['GET', 'POST'])
@login_required
def adddepartment():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        department.user = db_sess.query(User).get(form.chief.data)
        db_sess.add(department)
        department.user.departments.append(department)
        db_sess.merge(department.user)
        db_sess.commit()
        return flask.redirect('/departments')
    return flask.render_template('adddepartment.html', title='работы',
                           form=form)


@app.route('/editdepartment/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def editdepartment(department_id):
    form = AddDepartmentForm()
    if flask.request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            flask.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            department = db_sess.query(Department).get(department_id)
        else:
            department = db_sess.query(Department).filter(Department.id == department_id,
                                              departments.user == current_user,
                                              ).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return flask.redirect('/departments')
        else:
            flask.abort(404)
    return flask.render_template('adddepartment.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/deletedepartment/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def deletedepartment(department_id):
    db_sess = db_session.create_session()
    if current_user.id == 1:
        department = db_sess.query(Department).get(department_id)
    else:
        department = db_sess.query(Department).filter(Department.id == department_id,
                                         departments.user == current_user,
                                         ).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        flask.abort(404)

    return flask.redirect('/departments')





if __name__ == 'main':
    main()
