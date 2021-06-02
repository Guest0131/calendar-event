from flask import Flask, request, redirect, flash, url_for, session, render_template

from modules.check import *
from modules.calendar import Calendar

app = Flask(__name__)
app.secret_key = 'secret_key'

# Визуализация формы входа
@app.route('/', methods=['GET', 'POST'])
def index():
    if len(session) != 0:
        session.clear()

    return render_template('login.html')

# Обработка формы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if  request.method == 'POST':

        check = check_login(request.form)
        if check == False:
            flash("Введите корректные данные!")
            return redirect(url_for('index'))
        
        session['auth'] = True
        session['login'] = request.form['login']
        session['type'] = check

        # Переход на calendar
        return redirect(url_for('calendar'))

    if 'auth' not in session:
        return redirect(url_for('index'))
    
# Визуализация формы регистрации
@app.route('/reg')
def reg():
    return render_template('register.html')

# BackEnd формы визуализации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        check = check_register(request.form)
        if not check:
            flash('Пользователь с такими логином уже существует')
            return redirect(url_for('reg'))

        flash('Вы успешно зарегестрированы в системе. Теперь можете войти с используя свои данные')
        return redirect(url_for('index'))

    return redirect(url_for('reg'))


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    calendar = Calendar(session['login'])
    return render_template('calendar.html', name=calendar.name, data=calendar.get_data_dict()[session['login']])


@app.route('/api', methods=['GET', 'POST'])
def api():
    calendar = Calendar(session['login'])

    form = request.form.to_dict()
    print(form)
    if 'action' in form:
        action = form['action']
        if action == 'addEvent':
            calendar.add_event(form)
        elif action == 'editEvent':
            calendar.update_event(form)
        elif action == 'deleteEvent':
            calendar.deleteEvent(form)
    
    return ''

if __name__ == '__main__':
    app.run()