from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
from datetime import datetime

# Configuración de la app y base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reciclaje.db'
app.config['SECRET_KEY'] = 'mysecretkey'

# Inicialización de la base de datos
db = SQLAlchemy(app)

# Inicialización de LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Modelo de usuario
class User(UserMixin, db.Model):  # Usar UserMixin para implementar la funcionalidad de login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Agregamos la contraseña

    def __repr__(self):
        return f'<User {self.username}>'

# Modelo de actividad
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plastic_recycled = db.Column(db.Float, nullable=False)  # Plástico reciclado (kg)
    distance_walked = db.Column(db.Float, nullable=False)    # Distancia caminando (km)
    distance_biked = db.Column(db.Float, nullable=False)     # Distancia en bicicleta (km)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('activities', lazy=True))
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Activity {self.id} - User {self.user_id}>'

# Formulario de actividades
class ActivityForm(FlaskForm):
    plastic_recycled = FloatField('Cantidad de plástico reciclado (kg)', validators=[DataRequired()])
    distance_walked = FloatField('Distancia recorrida caminando (km)', validators=[DataRequired()])
    distance_biked = FloatField('Distancia recorrida en bicicleta (km)', validators=[DataRequired()])
    submit = SubmitField('Registrar Actividad')

# Formulario de registro de usuario
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

# Función que carga un usuario basado en su ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/delete_activity/<int:activity_id>', methods=['POST'])
@login_required
def delete_activity(activity_id):
    # Buscar la actividad por ID y usuario actual
    activity = Activity.query.filter_by(id=activity_id, user_id=current_user.id).first()

    if activity:
        db.session.delete(activity)
        db.session.commit()

    return redirect(url_for('profile'))  # Redirigir al perfil después de eliminar la actividad


# Ruta para el registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Verificar si el correo electrónico ya está registrado
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            # Si el correo ya existe, mostrar un mensaje de error
            return render_template('register.html', form=form, error="El correo electrónico ya está registrado.")
        
        # Crear un nuevo usuario
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)  # Iniciar sesión automáticamente
        return redirect(url_for('home'))  # Redirigir al inicio después de registrarse

    return render_template('register.html', form=form)

# Ruta para registrar actividades
@app.route('/register_activity', methods=['GET', 'POST'])
@login_required
def register_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        # Crear una nueva actividad
        activity = Activity(
            user_id=current_user.id,
            plastic_recycled=form.plastic_recycled.data,
            distance_walked=form.distance_walked.data,
            distance_biked=form.distance_biked.data,
            date=datetime.utcnow()
        )
        db.session.add(activity)
        db.session.commit()  # Asegúrate de hacer commit después de agregar la actividad

        return redirect(url_for('profile'))  # Redirigir al perfil después de registrar la actividad

    return render_template('register_activity.html', form=form)


# Ruta de inicio
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/sugerencias")
def sugerencias():
    return render_template("sugerencias.html")

# Ruta de perfil (muestra las actividades del usuario)
@app.route('/profile')
@login_required
def profile():
    # Obtener todas las actividades del usuario
    activities = Activity.query.filter_by(user_id=current_user.id).all()
    
    # Calcular el impacto total
    total_plastic_recycled = 0
    total_distance_walked = 0
    total_distance_biked = 0
    total_co2_saved = 0

    for activity in activities:
        total_plastic_recycled += activity.plastic_recycled
        total_distance_walked += activity.distance_walked
        total_distance_biked += activity.distance_biked
        total_co2_saved += activity.plastic_recycled * 1.5 + activity.distance_walked * 0.2 + activity.distance_biked * 0.1

    # Generar un mensaje personalizado basado en el CO₂ ahorrado
    co2_phone_charge = total_co2_saved / 5  # Suponiendo que 5 kg de CO₂ ahorrados equivalen a cargar un teléfono una vez
    co2_message = f"¡Has ahorrado suficiente CO₂ para cargar un teléfono {int(co2_phone_charge)} veces!"

    # Consejos para mejorar el impacto
    tips = [
        "Recicla más plástico. Cada kilogramo reciclado ayuda a reducir la contaminación.",
        "Camina más o usa la bicicleta en lugar del coche. Reducir el uso de vehículos ayuda a disminuir las emisiones de CO₂.",
        "Únete a iniciativas locales de reciclaje para promover el cambio en tu comunidad.",
        "Revisa y ajusta tu consumo energético en casa para reducir tu huella de carbono."
    ]

    # Pasar las actividades, impacto total, mensaje y consejos a la plantilla
    return render_template('profile.html', 
                           activities=activities, 
                           total_plastic_recycled=total_plastic_recycled,
                           total_distance_walked=total_distance_walked,
                           total_distance_biked=total_distance_biked,
                           total_co2_saved=total_co2_saved,
                           co2_message=co2_message,
                           tips=tips)


# Ruta de impacto ambiental
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@app.route('/impact')
def impact():
    activities = Activity.query.all()

    # Recalcular el impacto después de eliminar o agregar actividades
    total_plastic_recycled = 0
    total_distance_walked = 0
    total_distance_biked = 0
    total_co2_saved = 0

    for activity in activities:
        total_plastic_recycled += activity.plastic_recycled
        total_distance_walked += activity.distance_walked
        total_distance_biked += activity.distance_biked
        total_co2_saved += activity.plastic_recycled * 1.5 + activity.distance_walked * 0.2 + activity.distance_biked * 0.1

    # Crear gráfico de impacto
    labels = ['Plástico Reciclado', 'Distancia Caminando', 'Distancia en Bicicleta', 'CO₂ Ahorrado']
    values = [total_plastic_recycled, total_distance_walked, total_distance_biked, total_co2_saved]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['green', 'blue', 'orange', 'red'])
    ax.set_ylabel('Cantidad')
    ax.set_title('Impacto Ambiental Total')

    # Ajustar las etiquetas
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)

    # Convertir el gráfico a base64 para mostrarlo en el frontend
    output = BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    img_data = base64.b64encode(output.getvalue()).decode()

    return render_template('impact.html', 
                           total_plastic_recycled=total_plastic_recycled, 
                           total_distance_walked=total_distance_walked, 
                           total_distance_biked=total_distance_biked, 
                           total_co2_saved=total_co2_saved,
                           img_data=img_data)

# Función para crear las tablas en la base de datos
def recreate_tables():
    with app.app_context():
        db.drop_all()  # Elimina las tablas existentes
        db.create_all()  # Crea las tablas nuevamente

# Crear las tablas de la base de datos cuando se ejecuta la aplicación
# Crear las tablas de la base de datos solo si se está en desarrollo
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si aún no existen
    app.run(debug=True)

