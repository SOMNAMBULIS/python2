from flask import Flask, render_template, redirect, request, url_for, session
import os, requests, re

BASE_DIR = os.path.dirname(__name__)
app = Flask(__name__, template_folder=os.path.join(BASE_DIR,'templates'))
app.config['SECRET_KEY'] = 'secret'
login = ''
user_name= ''

def check_login(func):
    def wrapper(*args,**kwargs):
        if not login:
            return redirect('login')
            #return render_template('error.html')
        print(args,kwargs)
        return func(*args,**kwargs)
    return wrapper
    
def add_user(login,password,email,age,first_name, last_name):
    with open(file='user.txt', mode='a') as f:
        f.write(f'login:{login},password:{password},email:{email},age:{age},first_name:{first_name},last_name:{last_name}\n')

def check(name, password = '', mode = False):
    with open(file='user.txt', mode='r', encoding='UTF-8') as f:
        for i in f:
            i = dict(l.split(':') for l in i[:-1].split(','))
            if i['login'] == name and (i['password'] == password or mode):
                return True
    return False

@app.route('/')
def index():
    return render_template('index.html',login = login)

@app.route('/duct/', endpoint='duct')
@check_login
def duct():
    href = requests.get('https://random-d.uk/api/random').json()
    return render_template('duct.html', href = href['url'], num = href['url'].split('.')[1].split('/')[-1],login = login)

@app.route('/fox/<int:num>/', endpoint='fox')
@check_login
def fox(num):
    href = []
    if 0<num<11:
        href = [requests.get('https://randomfox.ca/floof/').json()['image'] for _ in range(num)]
    return render_template('fox.html',href = href, login = login)

@app.route('/weather/<city>/', methods = ['GET', 'POST'], endpoint = 'weather')
@check_login
def weather(city):
    if request.method == 'POST':
        city = request.form.get('city')
    url = f'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city.lower(), 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
    res = requests.get(url, params).json()
    if res['cod'] != '404':
        return render_template('weather.html',city = city.capitalize(), weather_=res['weather'][0]['main'], temp = int(res['main']['temp'])-273, login = login)
    else:
        return render_template('weather.html',error = True,city = city.capitalize(), login = login)

@app.route('/login/', methods = ['GET', 'POST'])
def login_():
    global login, user_name
    if request.method == 'POST':
        if check(request.form.get('login'), request.form.get('password')):
            login = request.form.get('login')
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    err = {}
    l = {}
    if request.method == 'POST':
        l = {'first_name':request.form.get('first_name'),'last_name':request.form.get('last_name'),'login':request.form.get('login'),'password':request.form.get('password1'),'email':request.form.get('email'),'age':request.form.get('age')}
        if not re.search(r'^[а-яА-Я]+$',l['first_name']):
            err['first_name'] = l['first_name']
        if not re.search(r'^[а-яА-Я]+$',l['last_name']):
            err['last_name'] = l['last_name']
        if not re.search(r'[a-zA_Z_]{6,20}$',l['login']):
            err['login'] = l['login']
        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z0-9]{8,15}$',request.form.get('password1')):
            err['password1'] = request.form.get('password1')
        if request.form.get('password1') != request.form.get('password2'):
            err['password2'] = request.form.get('password2')
        if not re.search(r'^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+$',l['email']):
            err['email'] = l['email']
        if not 11<int(l['age'])<101:
            err['age'] = l['age']
        if check(l['login'], mode=True):
            err['copy'] = True
        if err != {}:
            return render_template('register.html', err = err,l = l)
        else:
            add_user(l['login'],l['password'],l['email'],l['age'],l['first_name'],l['last_name'])
            return redirect(url_for('login_'))
    return render_template('register.html', err = err,l = l)

@app.route('/unlogin/')
def unlogin():
    global login, user_name
    session['user'] = None
    login = False
    return redirect(url_for('index'))

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html')

def main():
    app.run()


if __name__ == "__main__":
    main()