from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User, LoginForm
from forms.user import RegisterForm
import random
import sqlite3
from data.quiz import Quiz
from forms.quizz import QuizForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/quiz.db")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_2228'


def main():
    db_session.global_init("db/quiz.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("base1.html")


@app.route('/create',  methods=['GET', 'POST'])
@login_required
def add_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        quiz = Quiz()
        quiz.id_user = form.id_user.data
        quiz.question = form.question.data
        quiz.variants = form.variants.data
        quiz.correct_answer = form.correct_answer.data
        current_user.quiz.append(quiz)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('quiz.html', job='Добавление новости',
                           form=form)

@app.route('/geography')
def geography():
    question = 'Вопросик'
    ans = ['1', '2', '3']
    ans_t = '4'
    return render_template('after_quiz.html', answers=ans, true_question=ans_t, question=question, long=len(ans))


def choice():
    n = random.randint(1, 60)
    con = sqlite3.connect('databaze')
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM data
               id = {n})""").fetchall()


def truth():
    pass


def lie():
    pass

@app.route('/start_quiz')
def chemistry():
    return "Тут будет викторина по химии"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()