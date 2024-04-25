from flask import Flask, render_template

app = Flask(__name__)


# @app.route('/')
# def index():
# return render_template('index.html')

@app.route('/start')
def index():
    return render_template('base1.html')


@app.route('/login')
def login():
    return 'Войти'


@app.route('/submit', methods=['POST'])
def submit_form():
    # Handle form submission logic here
    return "Начать игру"


@app.route('/register')
def register():
    return "Регистрация"


@app.route('/geography')
def geography():
    return "Тут будет викторина по географии"


@app.route('/chemistry')
def chemistry():
    return "Тут будет викторина по химии"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
