from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class WolfAlphaForm(FlaskForm):
    question = StringField('input', validators=[DataRequired()])
    answer = StringField('answer')
    submit = SubmitField('Send')