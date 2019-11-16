from flask import Flask, render_template, url_for, flash, redirect, session, request
from forms import RegistrationForm, LoginForm
from mySql import Base_datos

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretApp<'

# conectar Base de Datos
bd = Base_datos('localhost', 'root', '12345', 'myFlaskApp')


@app.route("/")
@app.route("/home")
def home():
    if request.method == 'POST':
        session.clear()
        bd.cerrar()

    if 'email' in session:
        return redirect(url_for('games'))
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            # base de datos - validar
            leer_email = bd.query(
                f'SELECT email FROM gameuser WHERE email="{email}"'
            )
            if leer_email != ():
                return render_template('registro.html')

                # registrar en la base de datos
            leer_email = bd.query(
                f'INSERT INTO gameuser VALUES(null,"{username}","{email}","{password}",1)'
            )
            return redirect(url_for('login'))
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            # base de datos - validar
            leer_email = bd.query(
                f'SELECT email FROM gameuser WHERE email="{email}"'
            )
            if leer_email != ():

                leer_email_password = bd.query(
                    f'SELECT email,password,username FROM gameuser WHERE email="{email}"')

                if leer_email_password[0][0] == email and leer_email_password[0][1] == password:
                    # iniciar session
                    session['nombre'] = leer_email_password[0][2]
                    session['email'] = email
                    session['password'] = password

                    return redirect(url_for('games'))

            return render_template('login.html')

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/games")
def games():
    display_data = bd.query(f'SELECT u.username,p.puntos FROM gameuser AS u INNER JOIN puntos AS p ON u.ID_gameUser = p.ID_gameUser')
    random_world = bd.query(f'SELECT Tema , palabra FROM palabras ORDER BY RAND() LIMIT 1;')
    data_name = display_data[0][0]
    data_puntos = display_data[0][1]
    world_teme = random_world[0][0]
    world_content = random_world[0][1]
    return render_template('games.html', title='games', data_name=data_name, data_puntos=data_puntos,  world_content= world_content )


if __name__ == '__main__':
    app.run(debug=True)
