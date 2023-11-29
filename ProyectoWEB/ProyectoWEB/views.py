from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from ProyectoWEB import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://servidor:armando@(localdb)\\Servidor/SERVIDORSQL?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)

class Resena(db.Model):
    id_resena = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now())
    contenido = db.Column(db.String(1000), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    nombre_usuario = db.Column(db.String(50))
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id_pelicula'))
    
    usuario = db.relationship('Usuario', backref=db.backref('resenas', lazy=True))
    pelicula = db.relationship('Pelicula', backref=db.backref('resenas', lazy=True))

class Pelicula(db.Model):
    id_pelicula = db.Column(db.Integer, primary_key=True)
    sinopsis = db.Column(db.String(1000), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    clasificacion = db.Column(db.String(50))
    duracion = db.Column(db.Integer)
    fecha_estreno = db.Column(db.Date)

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
            return redirect(url_for('peliculas', user_name=usuario.nombre, user_id=usuario.id_usuario))
        else:
            return render_template('inicioSesion.html', title='Inicia Sesion', year=datetime.now().year)
    return render_template('inicioSesion.html', title='Inicia Sesion', year=datetime.now().year)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['correo']
            contrasena = request.form['contrasena']

            nuevo_usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena)
            db.session.add(nuevo_usuario)
            db.session.commit()

            return redirect(url_for('inicioSesion'))

        return render_template('registro.html', title='Regístrate', year=datetime.now().year)

    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500 

@app.route('/peliculas')
def peliculas():
    user_name = request.args.get('user_name')
    user_id = request.args.get('user_id')
    peliculas = Pelicula.query.all()
    print(user_id)
    return render_template('peliculas.html', title='Peliculas', year=datetime.now().year, peliculas=peliculas, user_name=user_name, user_id=user_id)

@app.route('/peliculas/<int:pelicula_id>/resenas', methods=['GET', 'POST'])
def resenas(pelicula_id):
    pelicula = Pelicula.query.get_or_404(pelicula_id)
    
    user_name = request.args.get('user_name')
    user_id = request.args.get('user_id')

    if request.method == 'POST':
        contenido = request.form['contenido']


        nueva_resena = Resena(
            contenido=contenido,
            id_usuario=user_id,
            nombre_usuario=user_name,
            id_pelicula=pelicula_id
        )

        db.session.add(nueva_resena)
        db.session.commit()

        return redirect(url_for('resenas', pelicula_id=pelicula_id, user_name=user_name, user_id=user_id))


    reseñas_pelicula = Resena.query.filter_by(id_pelicula=pelicula_id).all()

    return render_template('resenas.html', title=f"Reseñas de {pelicula.nombre}", year=datetime.now().year, pelicula=pelicula, reseñas=reseñas_pelicula, user_name=user_name, user_id=user_id)

@app.route('/peliculas/<int:pelicula_id>/resenas/<int:resena_id>/eliminar', methods=['POST'])
def eliminar_resena(pelicula_id, resena_id):

    user_name = request.args.get('user_name')
    user_id = int(request.args.get('user_id'))


    resena = Resena.query.get_or_404(resena_id)

    if resena.id_usuario != user_id:
        return redirect(url_for('resenas', pelicula_id=pelicula_id, user_name=user_name, user_id=user_id))


    db.session.delete(resena)
    db.session.commit()

    return redirect(url_for('resenas', pelicula_id=pelicula_id, user_name=user_name, user_id=user_id))