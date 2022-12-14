from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

#Configuracion de la DB

USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inicializacion del objeto db de sqlalchemy
db = SQLAlchemy(app)


#configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

#configuracion de flask-wtf
app.config['SECRET_KEY']='llave_secreta'

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))

    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'Nombre: {self.nombre}, '
            f'Apellido: {self.apellido}, '
            f'Email: {self.email}'
        )

class PersonaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    nombre = StringField('Apellido')
    nombre = StringField('Email', validators=[DataRequired])
    enviar = SubmitField('Enviar')

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #Listado de personas
    personas = Persona.query.all()
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    #Recuperamos la personas segun el id proporcionado
    #persona = Persona.query.get(id)
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona=persona)

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    persona = Persona()

# Refactorizacion video 546
