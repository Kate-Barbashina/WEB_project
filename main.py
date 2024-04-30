from flask import Flask, render_template, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User, LoginForm
from forms.user import RegisterForm
from random import *
import sqlite3
from data.quiz import Quiz
from forms.quizz import QuizForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/quiz.db")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_2228'
cnt_geo = 0
MAX_CNT_GEO = 0
cnt_che = 0
MAX_CNT_CHE = 0


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

@app.route('/before_geography', methods=['POST', 'GET'])
def before_geography():
    global MAX_CNT_GEO
    global cnt_geo
    cnt_geo = 0
    MAX_CNT_GEO = 0
    if request.method == 'GET':
        return render_template('before_geographe.html')
    elif request.method == 'POST':
        MAX_CNT_GEO = int(request.form['number'])
        n = 0
        con = sqlite3.connect('databaze.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM data""").fetchall()
        shuffle(result)
        question = result[0][0]
        ans = [i for i in result[0][1].split()]
        shuffle(ans)
        ans_t = str(result[0][2])
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return render_template('geography_quiz.html', time=time, answers=ans, true_question=ans_t, question=question, long=len(ans))


@app.route('/geography')
def geography():
    global MAX_CNT_GEO
    global cnt_geo
    cnt_geo += 1
    if cnt_geo == MAX_CNT_GEO:
        return render_template('end.html')
    else:
        n = 0
        con = sqlite3.connect('databaze.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM data""").fetchall()
        shuffle(result)
        question = result[0][0]
        ans = [i for i in result[0][1].split()]
        shuffle(ans)
        ans_t = str(result[0][2])
        return render_template('geography_quiz.html', answers=ans, true_question=ans_t, question=question, long=len(ans))


@app.route('/end')
def end():
    return render_template('end.html')


@app.route('/before_chemistry', methods=['POST', 'GET'])
def before_chemistry():
    global MAX_CNT_CHE
    global cnt_che
    cnt_che = 0
    MAX_CNT_CHE = 0
    if request.method == 'GET':
        return render_template('before_chemistry.html')
    elif request.method == 'POST':
        MAX_CNT_CHE = int(request.form['number'])
        con = sqlite3.connect('chem.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM chemistry""").fetchall()
        shuffle(result)
        question = result[0][0]
        ans = [i for i in result[0][1].split()]
        shuffle(ans)
        ans_t = str(result[0][2])
        return render_template('chemistry_quiz.html', answers=ans, true_question=ans_t, question=question, long=len(ans))


@app.route('/chemistry')
def chemistry():
    global MAX_CNT_CHE
    global cnt_che
    cnt_che += 1
    if cnt_che == MAX_CNT_CHE:
        return render_template('end.html')
    else:
        con = sqlite3.connect('chem.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM chemistry""").fetchall()
        shuffle(result)
        question = result[0][0]
        ans = [i for i in result[0][1].split()]
        shuffle(ans)
        ans_t = str(result[0][2])
        return render_template('chemistry_quiz.html', answers=ans, true_question=ans_t, question=question, long=len(ans))


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