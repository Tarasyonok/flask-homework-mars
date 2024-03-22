import flask
from flask import request, jsonify, make_response, redirect

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify(
        {'jobs': [str(item.to_dict()) for item in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'job': job.to_dict()})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    required_columns = ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in required_columns):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()

    kwargs = {}
    for key in required_columns:
        kwargs[key] = request.json[key]
    print(kwargs)

    job = Jobs(**kwargs)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    print("!!!!!!!!!DELETING!!!!!!!!!!")
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return make_response(jsonify({'success': 'OK'}))


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    required_columns = ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in required_columns):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    print(job)

    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']

    db_sess.commit()
    return make_response(jsonify({'id': job.id}))