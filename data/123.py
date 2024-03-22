@app.route('/adddepartment/',  methods=['GET', 'POST'])
@login_required
def adddepartment():
    form = AdddepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = departments()
        department.department = form.department.data
        department.team_leader = form.team_leader.data
        department.work_size = form.work_size.data
        department.collaborators = form.collaborators.data
        department.is_finished = form.is_finished.data
        local_user = db_sess.merge(current_user)
        department.creator = local_user
        # local_object = db_session.merge(original_object)
        db_sess.add(department)
        db_sess.commit()
        return flask.redirect('/')
    return flask.render_template('adddepartment.html', title='работы',
                           form=form)


@app.route('/editdepartment/<int:department_id>/', methods=['GET', 'POST'])
@login_required
def editdepartment(department_id):
    form = AdddepartmentForm()
    if flask.request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(departments).filter(departments.id == department_id).first()
        if department:
            form.department.data = department.department
            form.team_leader.data = department.team_leader
            form.work_size.data = department.work_size
            form.collaborators.data = department.collaborators
            form.is_finished.data = department.is_finished
        else:
            flask.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            department = db_sess.query(departments).get(department_id)
        else:
            department = db_sess.query(departments).filter(departments.id == department_id,
                                              departments.creator == current_user,
                                              ).first()
        if department:
            department.department = form.department.data
            department.team_leader = form.team_leader.data
            department.work_size = form.work_size.data
            department.collaborators = form.collaborators.data
            department.is_finished = form.is_finished.data
            db_sess.commit()
            return flask.redirect('/')
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
        department = db_sess.query(departments).get(department_id)
    else:
        department = db_sess.query(departments).filter(departments.id == department_id,
                                         departments.creator == current_user,
                                         ).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        flask.abort(404)

    return flask.redirect('/')

