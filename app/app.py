import os
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://postgres:postgres@db:5432/authdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def create_tables():
    with app.app_context():
        for attempt in range(1, 11):
            try:
                db.create_all()
                return
            except Exception:
                if attempt == 10:
                    raise
                time.sleep(2)


@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if not username or not password:
            flash('Por favor, completa todos los campos.', 'warning')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Usuario o contraseña incorrectos. Intenta de nuevo.', 'danger')
            return render_template('login.html', username=username)

        session['username'] = user.username
        flash('Inicio de sesión exitoso.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if not username or not password or not password_confirm:
            flash('Por favor, completa todos los campos.', 'warning')
            return render_template('register.html')

        if password != password_confirm:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('register.html', username=username)

        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe. Elige otro nombre.', 'danger')
            return render_template('register.html', username=username)

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        flash('Usuario registrado correctamente. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    create_tables()
    context = ('certs/server.crt', 'certs/server.key')
    app.run(host='0.0.0.0', port=443, ssl_context=context)
