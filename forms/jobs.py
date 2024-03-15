from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = wtforms.StringField('Job title', validators=[DataRequired()])
    team_leader = wtforms.IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = wtforms.IntegerField('Work size', validators=[DataRequired()])
    collaborators = wtforms.StringField('Collaborators', validators=[DataRequired()])
    is_finished = wtforms.BooleanField("Is job finished?")
    submit = wtforms.SubmitField('Submit')
