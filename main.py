import sqlite3
from random import *

import requests
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.quiz import Quiz
from data.users import User, LoginForm
from forms.quizz import QuizForm
from forms.user import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/quiz.db")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_2228'
cnt_geo, cnt_che, cnt_er, cnt_us = 0, 0, 0, 0
MAX_CNT_GEO, MAX_CNT_CHE, MAX_CNT_ER, MAX_CNT_US = 0, 0, 0, 0
CORRECT_GEO, CORRECT_CHE, CORRECT_ER, CORRECT_US = 0, 0, 0, 0

def geo_extra():
    map_request = "https://static-maps.yandex.ru/1.x/?ll=137.685869,-27.182713&spn=20.116457,20.10619&l=sat"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
    map_file = "static/img/map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
        file.close()


def main():
    db_session.global_init("db/quiz.db")
    geo_extra()
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("base1.html")


@app.route('/create', methods=['GET', 'POST'])
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
        con = sqlite3.connect('geo.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM quiz""").fetchall()
        shuffle(result)
        question = result[0][1]
        ans = [i for i in result[0][2].split(',')]
        ans_t = str(result[0][3])
        ans.append(ans_t)
        shuffle(ans)
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if question == 'Какой континент изображен на картинке':
            return render_template('geography_quiz_img.html', time=time, answers=ans, true_question=ans_t, question=question,
                               long=len(ans))
        else:
            return render_template('geography_quiz.html', time=time, answers=ans, true_question=ans_t,
                                   question=question,
                                   long=len(ans))


@app.route('/geography')
def geography():
    global cnt_geo
    global CORRECT_GEO
    cnt_geo += 1
    if cnt_geo == MAX_CNT_GEO:
        if CORRECT_GEO == MAX_CNT_GEO:
            CORRECT_GEO = 0
            return render_template('end_ura.html')
        else:
            true_answer = CORRECT_GEO
            false_answer = MAX_CNT_GEO - CORRECT_GEO
            CORRECT_GEO = 0
            return render_template('end_ne_ura.html', true_answer=true_answer, false_answer=false_answer)
    else:
        n = 0
        con = sqlite3.connect('geo.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM quiz""").fetchall()
        shuffle(result)
        question = result[0][1]
        ans = [i for i in result[0][2].split(',')]
        ans_t = str(result[0][3])
        ans.append(ans_t)
        shuffle(ans)
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if question == 'Какой континент изображен на картинке':
            return render_template('geography_quiz_img.html', time=time, answers=ans, true_question=ans_t,
                                   question=question,
                                   long=len(ans))
        else:
            return render_template('geography_quiz.html', time=time, answers=ans, true_question=ans_t,
                                   question=question,
                                   long=len(ans))

@app.route('/geography_true')
def geography_true():
    global cnt_geo
    global CORRECT_GEO
    CORRECT_GEO += 1
    cnt_geo += 1
    if cnt_geo == MAX_CNT_GEO:
        if CORRECT_GEO == MAX_CNT_GEO:
            CORRECT_GEO = 0
            return render_template('end_ura.html')
        else:
            true_answer = CORRECT_GEO
            false_answer = MAX_CNT_GEO - CORRECT_GEO
            CORRECT_GEO = 0
            return render_template('end_ne_ura.html', true_answer=true_answer, false_answer=false_answer)
    else:
        n = 0
        con = sqlite3.connect('geo.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM quiz""").fetchall()
        shuffle(result)
        question = result[0][1]
        ans = [i for i in result[0][2].split(',')]
        ans_t = str(result[0][3])
        ans.append(ans_t)
        shuffle(ans)
        return render_template('geography_quiz.html', answers=ans, true_question=ans_t, question=question,
                               long=len(ans))


@app.route('/end')
def end():
    global CORRECT_ER
    global CORRECT_GEO
    global CORRECT_CHE
    global CORRECT_US
    if CORRECT_CHE == MAX_CNT_CHE or CORRECT_GEO == MAX_CNT_GEO or CORRECT_ER == MAX_CNT_ER or MAX_CNT_US == CORRECT_US:
        CORRECT_GEO, CORRECT_CHE, CORRECT_ER, CORRECT_US = 0, 0, 0, 0
        return render_template('end_ura.html')
    if CORRECT_CHE != MAX_CNT_CHE:
        true_answer = CORRECT_CHE
        false_answer = MAX_CNT_CHE - CORRECT_CHE
        CORRECT_CHE = 0
        return render_template('end_ne_ura.html', true_answer=true_answer, false_answer=false_answer)
    if CORRECT_GEO != MAX_CNT_GEO:
        true_answer = CORRECT_GEO
        false_answer = MAX_CNT_GEO - CORRECT_GEO
        CORRECT_GEO = 0
        return render_template('end_ne_ura.html',  true_answer=true_answer, false_answer=false_answer)
    if CORRECT_ER != MAX_CNT_ER:
        true_answer = CORRECT_ER
        false_answer = MAX_CNT_ER - CORRECT_ER
        CORRECT_ER = 0
        return render_template('end_ne_ura.html',  true_answer=true_answer, false_answer=false_answer)
    if CORRECT_US != MAX_CNT_US:
        true_answer = CORRECT_US
        false_answer = MAX_CNT_US - CORRECT_US
        CORRECT_US = 0
        return render_template('end_ne_ura.html',  true_answer=true_answer, false_answer=false_answer)



@app.route('/before_users', methods=['POST', 'GET'])
def before_users():
    global MAX_CNT_US
    global cnt_us
    cnt_us = 0
    MAX_CNT_US = 0
    if request.method == 'GET':
        return render_template('before_users.html')
    elif request.method == 'POST':
        MAX_CNT_US = int(request.form['number'])
        n = 0
        con = sqlite3.connect('db/quiz.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM quiz""").fetchall()
        shuffle(result)
        question = result[0][2]
        ans = [i for i in result[0][3].split(',')]
        ans_t = str(result[0][4])
        ans.append(ans_t)
        shuffle(ans)
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return render_template('users_quiz.html', time=time, answers=ans, true_question=ans_t, question=question,
                               long=len(ans))


@app.route('/users')
def users():
    global cnt_us
    global CORRECT_US
    cnt_us += 1
    if cnt_us == MAX_CNT_US:
        if CORRECT_US == MAX_CNT_US:
            CORRECT_US = 0
            return render_template('end_ura.html')
        else:
            true_answer = CORRECT_US
            false_answer = MAX_CNT_US - CORRECT_US
            CORRECT_US = 0
            return render_template('end_ne_ura.html', true_answer=true_answer, false_answer=false_answer)
    else:
        n = 0
        con = sqlite3.connect('db/quiz.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM quiz""").fetchall()
        shuffle(result)
        question = result[0][2]
        ans = [i for i in result[0][3].split(',')]
        ans_t = str(result[0][4])
        ans.append(ans_t)
        shuffle(ans)
        return render_template('users_quiz.html', answers=ans, true_question=ans_t, question=question,
                               long=len(ans))


@app.route('/users_true')
def users_true():
    global cnt_us
    global CORRECT_US
    CORRECT_US += 1
    cnt_us += 1
    if cnt_us == MAX_CNT_US:
        if CORRECT_US == MAX_CNT_US:
            CORRECT_US = 0
            return render_template('end_ura.html')
        else:
            true_answer = CORRECT_US
            false_answer = MAX_CNT_US - CORRECT_US
            CORRECT_US = 0
            return render_template('end_ne_ura.html', true_answer=true_answer, false_answer=false_answer)
    else:
        n = 0
        con = sqlite3.connect('db/quiz.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM quiz""").fetchall()
        shuffle(result)
        question = result[0][2]
        ans = [i for i in result[0][3].split()]
        ans_t = str(result[0][4])
        ans.append(ans_t)
        shuffle(ans)
        return render_template('users_quiz.html', answers=ans, true_question=ans_t, question=question,
                               long=len(ans))


@app.route('/before_erudition', methods=['POST', 'GET'])
def before_erudition():
    global MAX_CNT_ER
    global cnt_er
    cnt_er = 0
    if request.method == 'GET':
        return render_template('before_erudition.html')
    elif request.method == 'POST':
        MAX_CNT_ER = int(request.form['time'])
        n = 0
        con = sqlite3.connect('databaze.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM data""").fetchall()
        shuffle(result)
        question = result[0][0]
        ans = [i for i in result[0][1].split(',')]
        shuffle(ans)
        ans_t = str(result[0][2])
        time = MAX_CNT_ER
        return render_template('erudition_quiz.html', time=time, answers=ans, true_question=ans_t, question=question,
                               long=len(ans))


@app.route('/erudition')
def erudition():
    global cnt_er
    cnt_er += 1
    time = MAX_CNT_ER
    n = 0
    con = sqlite3.connect('databaze.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM data""").fetchall()
    shuffle(result)
    question = result[0][0]
    ans = [i for i in result[0][1].split(',')]
    shuffle(ans)
    ans_t = str(result[0][2])
    return render_template('erudition_quiz.html', time=time, answers=ans, true_question=ans_t, question=question,
                           long=len(ans))

@app.route('/erudition_true')
def erudition_true():
    global cnt_er
    global CORRECT_ER
    CORRECT_ER += 1
    cnt_er += 1
    time = MAX_CNT_ER
    n = 0
    con = sqlite3.connect('databaze.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM data""").fetchall()
    shuffle(result)
    question = result[0][0]
    ans = [i for i in result[0][1].split(',')]
    shuffle(ans)
    ans_t = str(result[0][2])
    return render_template('erudition_quiz.html', time=time, answers=ans, true_question=ans_t, question=question,
                           long=len(ans))

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
        if question == 'Пламя какого элемента изображено на картинке':
            return render_template('chemistry_quiz_img.html', answers=ans, true_question=ans_t, question=question,
                                   long=len(ans))
        else:
            return render_template('chemistry_quiz.html', answers=ans, true_question=ans_t, question=question,
                                   long=len(ans))


@app.route('/chemistry')
def chemistry():
    global cnt_che
    global CORRECT_CHE
    cnt_che += 1
    if cnt_che == MAX_CNT_CHE:
        if CORRECT_CHE == MAX_CNT_CHE:
            CORRECT_CHE = 0
            return render_template('end_ura.html')
        else:
            true_answer = CORRECT_CHE
            false_answer = MAX_CNT_CHE - CORRECT_CHE
            CORRECT_CHE = 0
            return render_template('end_ne_ura.html', true_answer=true_answer, false_answer=false_answer)
    else:
        con = sqlite3.connect('chem.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM chemistry""").fetchall()
        shuffle(result)
        question = result[0][0]
        ans = [i for i in result[0][1].split()]
        shuffle(ans)
        ans_t = str(result[0][2])
        if question == 'Пламя какого элемента изображено на картинке':
            return render_template('chemistry_quiz_img.html', answers=ans, true_question=ans_t, question=question,
                                   long=len(ans))
        else:
            return render_template('chemistry_quiz.html', answers=ans, true_question=ans_t, question=question,
                                   long=len(ans))

@app.route('/chemistry_true')
def chemistry_true():
    global CORRECT_CHE
    CORRECT_CHE += 1
    global cnt_che
    cnt_che += 1
    if cnt_che == MAX_CNT_CHE:
        if CORRECT_CHE == MAX_CNT_CHE:
            CORRECT_CHE = 0
            return render_template('end_ura.html')
        else:
            true_answer = CORRECT_CHE
            false_answer = MAX_CNT_CHE - CORRECT_CHE
            CORRECT_CHE = 0
            return render_template('end_ne_ura.html', true_answer=true_answer, false_answer=false_answer)
    else:
        con = sqlite3.connect('chem.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM chemistry""").fetchall()
        shuffle(result)
        question = result[0][0]
        ans = [i for i in result[0][1].split()]
        shuffle(ans)
        ans_t = str(result[0][2])
        if question == 'Пламя какого элемента изображено на картинке':
            return render_template('chemistry_quiz_img.html', answers=ans, true_question=ans_t, question=question,
                                   long=len(ans))
        else:
            return render_template('chemistry_quiz.html', answers=ans, true_question=ans_t, question=question,
                                   long=len(ans))



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
