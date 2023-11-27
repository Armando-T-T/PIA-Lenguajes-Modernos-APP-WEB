from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from ProyectoWEB import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sistema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id_Usuario = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(255))
    correo = db.Column(db.String(255), unique=True)
    contrasena = db.Column(db.String(255))

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Bienvenido',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/inicioSesion', methods=['GET', 'POST'])
def inicioSesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        usuario = Usuario.query.filter_by(correo=correo, contrasena=contrasena).first()

        if usuario:
            return redirect(url_for('home'))
        else:
            return render_template('inicioSesion.html', title='Inicia Sesion', year=datetime.now().year)
    return render_template('inicioSesion.html', title='Inicia Sesion', year=datetime.now().year)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['correo']
            contrasena = request.form['contrasena']  # Asegúrate de que el nombre de la columna sea correcto

            nuevo_usuario = Usuario(Nombre=nombre, correo=correo, contrasena=contrasena)
            db.session.add(nuevo_usuario)
            db.session.commit()

            return redirect(url_for('home'))

        return render_template('registro.html', title='Regístrate', year=datetime.now().year)

    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500  # Devuelve un código de estado 500 (Internal Server Error)
