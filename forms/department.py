from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired


class AddDepartmentForm(FlaskForm):
    title = wtforms.StringField('Department title', validators=[DataRequired()])
    chief = wtforms.IntegerField('Chief id', validators=[DataRequired()])
    members = wtforms.StringField('Members', validators=[DataRequired()])
    email = wtforms.EmailField('Email', validators=[DataRequired()])
    submit = wtforms.SubmitField('Submit')
