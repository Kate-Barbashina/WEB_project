from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    id_user = StringField('id создателя', validators=[DataRequired()])
    question = StringField('Вопрос', validators=[DataRequired()])
    variants = StringField('Все варианты ответов, кроме верного', validators=[DataRequired()])
    correct_answer = StringField('Верный ответ', validators=[DataRequired()])
    submit = SubmitField('Применить')