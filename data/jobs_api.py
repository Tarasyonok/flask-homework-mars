import flask
from flask import request, jsonify, make_response

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
def get_one_jobs(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'job': job.to_dict()})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
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

    jobs = Jobs(**kwargs)
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})
