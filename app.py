# app.py
from flask import Flask, request, redirect, render_template, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests
from sqlalchemy import text, Enum
from sqlalchemy.exc import IntegrityError
import random
from cryptography.fernet import Fernet
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
import os
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ✅ Create folder if not present
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

SECRET_ENCRYPTION_KEY = b'5NGzLRD-kXqEhHuqQi9LbPZ2xhobG9oXGd2jaB3K-SU='  # Replace with your real key

fernet = Fernet(SECRET_ENCRYPTION_KEY)
app.secret_key = 'your_secret_key_here'
def generate_rsa_keys():
    # Dummy RSA key generation for demo purposes
    e = 65537
    d = 1234567890123456789012345678901234567890  # placeholder
    n = 9876543210987654321098765432109876543210  # placeholder
    return e, d, n
@app.template_filter('decrypt')
def decrypt_filter(token):
    return decrypt_message(token)
@app.template_filter('encrypt')
def encrypt_filter(message):
    return encrypt_message(message)

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        custom_id = request.form['custom_id']
        full_name = request.form['full_name']
        specialization = request.form['specialization']
        phone = request.form['phone']
        experience = request.form['experience']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']

        e, d, n = generate_rsa_keys()

        new_doctor = Doctor(
            custom_id=custom_id,
            full_name=full_name,
            specialization=specialization,
            phone=phone,
            experience=experience,
            gender=gender,
            email=email,
            password=password,
            public_key_e=e,
            private_key_d=d,
            modulus_n=n
        )

        try:
            db.session.add(new_doctor)
            db.session.commit()
            flash('Doctor registered successfully with RSA keys generated.')
            return redirect(url_for('doctor_login'))
        except Exception as ex:
            db.session.rollback()
            flash(f'Error: {ex}')
            return redirect(url_for('register_doctor'))

    return render_template('register_doctor.html')
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        identifier = request.form.get('email')

        # Check all user models to find a match
        for role, model in {
            'patient': Patient,
            'admin': Admin,
            'lab': Lab,
            'hospital': Hospital
        }.items():
            phone_field = getattr(model, 'contact_number', getattr(model, 'phone', None))
            user = model.query.filter((model.email == identifier) | (phone_field == identifier)).first()

            if user:
                otp = str(random.randint(1000, 9999))
                session['otp'] = otp
                session['reset_user'] = user.custom_id
                session['reset_role'] = role
                flash(f"Your OTP is: {otp}", "info")  # for dev only
                return redirect(url_for('verify_otp'))

        return "<script>alert('User not found'); window.history.back();</script>"

    return render_template('forgot.html')

    
@app.route('/success')
def success_page():
    user_id = request.args.get('user_id')
    return render_template('success.html', user_id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        role = request.form.get('role', '').lower().strip()

        # Define model and name field per role
        model_map = {
            'doctor': Doctor,
            'patient': Patient,
            'admin': Admin,
            'lab': Lab,
            'hospital': Hospital
        }

        field_map = {
            'doctor': 'full_name',
            'patient': 'full_name',
            'admin': 'full_name',
            'lab': 'name',
            'hospital': 'name'
        }

        model = model_map.get(role)
        name_field = field_map.get(role)

        if not model or not name_field:
            flash("Invalid role selected.", "danger")
            return redirect(url_for('login_page'))

        # Query the user by the appropriate name field
        try:
            user = model.query.filter_by(**{name_field: username}).first()
        except Exception as e:
            flash("Error occurred during login.", "danger")
            return redirect(url_for('login_page'))

        # Validate user credentials
        if user and user.password == password:
            session['custom_id'] = user.custom_id
            session['role'] = role
            return redirect(url_for(f"{role}_dashboard"))

        flash("Invalid credentials.", "danger")
        return redirect(url_for('login_page'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))



@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        if not session.get('otp') or not session.get('reset_user') or not session.get('reset_role'):
            return "<script>alert('Session expired. Please request OTP again.'); window.location='/forgot';</script>"

        entered_otp = request.form.get('otp', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if entered_otp != session.get('otp'):
            return "<script>alert('Invalid OTP'); window.history.back();</script>"

        if new_password != confirm_password:
            return "<script>alert('Passwords do not match'); window.history.back();</script>"

        if len(new_password) < 6:
            return "<script>alert('Password must be at least 6 characters long'); window.history.back();</script>"

        role = session.get('reset_role')
        user_id = session.get('reset_user')

        model_map = {
            'patient': Patient,
            'admin': Admin,
            'lab': Lab,
            'hospital': Hospital
        }
        model = model_map.get(role)
        user = model.query.get(user_id)

        if user:
            user.password = new_password
            db.session.commit()
            session.pop('otp', None)
            session.pop('reset_user', None)
            session.pop('reset_role', None)
            return "<script>alert('Password reset successful'); window.location='/login';</script>"

        return "<script>alert('User session expired or invalid.'); window.location='/forgot';</script>"

    return render_template('verify_otp.html')


# UTILITIES
def safe_register_user(model_class, role_prefix, data, max_retries=5):
    year_code = datetime.now().strftime('%y')
    prefix = role_prefix.upper()
    pattern = f"{prefix}{year_code}%"

    table_map = {
        'H': 'hospitals',
        'D': 'doctors',
        'L': 'labs',
        'A': 'admins',
        'P': 'patients'
    }

    table_name = table_map.get(prefix)
    if not table_name:
        raise ValueError("Invalid role prefix.")

    query = text(f"""
        SELECT custom_id 
        FROM {table_name} 
        WHERE custom_id LIKE :pattern
          AND LENGTH(custom_id) = 9
          AND custom_id REGEXP '^{prefix}{year_code}[A-Z][0-9]{{4}}$'
        ORDER BY custom_id DESC 
        LIMIT 1
    """)
    result = db.session.execute(query, {"pattern": pattern}).fetchone()

    if result and result[0]:
        last_id = result[0]
        letter = last_id[4]
        number = int(last_id[5:]) + 1
    else:
        letter = 'A'
        number = 1

    for _ in range(max_retries):
        try:
            if number > 9999:
                if letter == 'Z':
                    raise Exception("ID limit reached.")
                letter = chr(ord(letter) + 1)
                number = 1

            custom_id = f"{prefix}{year_code}{letter}{str(number).zfill(4)}"
            user = model_class(custom_id=custom_id, **data)
            db.session.add(user)
            db.session.commit()
            return custom_id
        except IntegrityError:
            db.session.rollback()
            number += 1

    raise Exception("Registration failed after multiple attempts.")

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        payload = {'secret': RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}
        recaptcha_result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload).json()

        if not recaptcha_result.get('success'):
            return "<script>alert('reCAPTCHA failed.'); window.history.back();</script>"

        role = request.form.get('usertype', '').strip().lower()
        if role == 'patient':
            return redirect(url_for('voice_register'))

        data = request.form
        username = data.get('name')
        email = data.get('email')
        gender = data.get(f"{role}_gender", '').lower().strip()
        country_code = data.get('country_code')
        phone = f"{country_code}{data.get('phone')}"

        password_fields = {
            'hospital': ('hospass', 'conhospass'),
            'doctor': ('docpass', 'condocpass'),
            'laboratory': ('labpass', 'conlabpass'),
            'admin': ('adipass', 'conadipass')
        }

        pass_key, conf_key = password_fields.get(role, (None, None))
        password = data.get(pass_key)
        confirm = data.get(conf_key)

        if not all([username, email, phone, role, gender, password, confirm]):
            return "<script>alert('All fields are required.'); window.history.back();</script>"

        if password != confirm:
            return "<script>alert('Passwords do not match.'); window.history.back();</script>"

        prefix_map = {
            'doctor': 'D',
            'laboratory': 'L',
            'hospital': 'H',
            'admin': 'A'
        }
        prefix = prefix_map.get(role)

        try:
            if role == 'hospital':
                data_dict = {
                    'name': username,
                    'contact_number': phone,
                    'designation': data.get('designation'),
                    'gender': gender,
                    'email': email,
                    'password': password
                }
                custom_id = safe_register_user(Hospital, prefix, data_dict)

            elif role == 'doctor':
                data_dict = {
                    'full_name': username,
                    'specialization': data.get('specialisation'),
                    'phone': phone,
                    'experience': data.get('experience'),
                    'gender': gender,
                    'email': email,
                    'password': password
                }
                custom_id = safe_register_user(Doctor, prefix, data_dict)

            elif role == 'laboratory':
                data_dict = {
                    'name': username,
                    'location': data.get('address'),
                    'contact_number': phone,
                    'gender': gender,
                    'email': email,
                    'password': password
                }
                custom_id = safe_register_user(Lab, prefix, data_dict)

            elif role == 'admin':
                data_dict = {
                    'full_name': username,
                    'access_level': 'full',
                    'gender': gender,
                    'email': email,
                    'contact_number': phone,
                    'password': password
                }
                custom_id = safe_register_user(Admin, prefix, data_dict)

            return render_template("success.html", user_id=custom_id)

        except Exception as e:
            return f"<script>alert('Registration failed: {str(e)}'); window.history.back();</script>"

    return render_template("registration.html")

@app.route('/voice_register', methods=['GET'])
def voice_register():
    return render_template('patient.html')

@app.route('/register_voice', methods=['POST'])
def register_voice():
    try:
        data = request.get_json()
        username = data.get('name')
        email = data.get('email')
        gender = data.get('gender')
        phone = data.get('contact')
        password = data.get('password')
        confirm = data.get('confirmPassword')
        age = int(data.get('age'))

        if not all([username, email, phone, gender, password, confirm, age]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        if password != confirm:
            return jsonify({"status": "error", "message": "Passwords do not match"}), 400

        data_dict = {
            'full_name': username,
            'gender': gender,
            'age': age,
            'contact_number': phone,
            'email': email,
            'password': password
        }
        custom_id = safe_register_user(Patient, 'P', data_dict)
        return jsonify({"status": "success", "custom_id": custom_id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

# DB and reCAPTCHA Config
RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/Bujji'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=60)

db = SQLAlchemy(app)

# Encryption setup
def encrypt_message(message):
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(token):
    try:
        return fernet.decrypt(token.encode()).decode()
    except Exception:
        return "[Decryption Failed]"
class PatientImageMessage(db.Model):
    __tablename__ = 'patient_image_messages'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), db.ForeignKey('patients.custom_id'), nullable=False)
    doctor_id = db.Column(db.String(20), db.ForeignKey('doctors.custom_id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='image_messages')
    doctor = db.relationship('Doctor', backref='patient_image_messages')

class Lab(db.Model):
    __tablename__ = 'labs'
    custom_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.Text, nullable=False)
    gender = db.Column(Enum('male', 'female', 'other'), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    contact_number = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
class LabImageMessage(db.Model):
    __tablename__ = 'lab_image_messages'
    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.String(20), db.ForeignKey('labs.custom_id'), nullable=False)
    doctor_id = db.Column(db.String(20), db.ForeignKey('doctors.custom_id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    lab = db.relationship('Lab', backref='sent_images')
    doctor = db.relationship('Doctor', backref='received_lab_images')

# MODELS
class Patient(db.Model):
    __tablename__ = 'patients'
    custom_id = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
# MODELS
class Hospital(db.Model):
    __tablename__ = 'hospitals'
    custom_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    gender = db.Column(Enum('male', 'female', 'other'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
class PatientImage(db.Model):
    __tablename__ = 'patient_images'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), db.ForeignKey('patients.custom_id'))
    image_path = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='images')

class LabDoctorMessage(db.Model):
    __tablename__ = 'lab_doctor_messages'

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.String(20), db.ForeignKey('labs.custom_id'), nullable=False)
    doctor_id = db.Column(db.String(20), db.ForeignKey('doctors.custom_id'), nullable=False)
    encrypted_message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    lab = db.relationship('Lab', backref='lab_sent_messages')
    doctor = db.relationship('Doctor', backref='lab_received_messages')

class Doctor(db.Model):
    __tablename__ = 'doctors'
    custom_id = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
class Admin(db.Model):
    __tablename__ = 'admins'
    custom_id = db.Column(db.String(20), primary_key=True)
    contact_number = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    access_level = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
class DoctorLabReplyMessage(db.Model):
    __tablename__ = 'doctor_lab_reply_messages'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.String(20), db.ForeignKey('doctors.custom_id'), nullable=False)
    lab_id = db.Column(db.String(20), db.ForeignKey('labs.custom_id'), nullable=False)
    reply_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class PatientDoctorMessage(db.Model):
    __tablename__ = 'patient_doctor_messages'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), db.ForeignKey('patients.custom_id'), nullable=False)
    doctor_id = db.Column(db.String(20), db.ForeignKey('doctors.custom_id'), nullable=False)
    encrypted_message = db.Column(db.Text, nullable=False)  # Message from patient
    reply_text = db.Column(db.Text)  # ✅ Message from doctor
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='messages')
    doctor = db.relationship('Doctor', backref='messages')


@app.route('/send_lab_reply', methods=['POST'])
def send_lab_reply():
    doctor_id = session['custom_id']
    lab_id = request.form['lab_id']
    reply_text = request.form['reply_text']

    reply = DoctorLabReplyMessage(
        doctor_id=doctor_id,
        lab_id=lab_id,
        reply_text=reply_text
    )
    db.session.add(reply)
    db.session.commit()

    flash("Reply sent to lab.", "success")
    return redirect(url_for('doctor_dashboard'))


@app.route('/send_lab_message', methods=['POST'])
def send_lab_message():
    if 'custom_id' not in session or session.get('role') != 'lab':
        return redirect(url_for('login_page'))

    lab_id = session['custom_id']
    doctor_id = request.form['doctor_id']
    message = request.form['message']

    encrypted_msg = encrypt_message(message)

    msg = LabDoctorMessage(
        lab_id=lab_id,
        doctor_id=doctor_id,
        encrypted_message=encrypted_msg
    )
    db.session.add(msg)
    db.session.commit()

    flash("Message sent to doctor!", "success")
    return redirect(url_for('lab_dashboard'))

# PATIENT DASHBOARD
# PATIENT SEND MESSAGE
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'custom_id' not in session:
        return redirect(url_for('login_page'))

    patient_id = session['custom_id']
    doctor_id = request.form['doctor_id']
    message = request.form.get('message')
        # Encrypt and save message
    if message:
        encrypted_msg = encrypt_message(message)
        msg = PatientDoctorMessage(
            patient_id=patient_id,
            doctor_id=doctor_id,
            encrypted_message=encrypted_msg
        )
        db.session.add(msg)

    # Handle image upload
    file = request.files.get('image')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(saved_path)

        image_msg = PatientImageMessage(
            patient_id=patient_id,
            doctor_id=doctor_id,
            image_path=saved_path
        )
        db.session.add(image_msg)

    db.session.commit()
    flash("Message and/or image sent!", "success")
    return redirect(url_for('patient_dashboard'))
@app.route('/lab_dashboard', methods=['GET', 'POST'])
def lab_dashboard():
    if 'custom_id' not in session or session.get('role') != 'lab':
        return redirect(url_for('login_page'))

    lab_id = session['custom_id']
    lab = Lab.query.get(lab_id)
    doctors = Doctor.query.all()

    # FETCH REPLIES sent by doctors to this lab
    replies = DoctorLabReplyMessage.query.filter_by(lab_id=lab_id).order_by(DoctorLabReplyMessage.timestamp.desc()).all()

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        image = request.files.get('image')

        if image and image.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            filename = f"{lab_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{image.filename}"
            path = os.path.join('static/uploads', filename)
            image.save(path)

            lab_image = LabImageMessage(
                lab_id=lab_id,
                doctor_id=doctor_id,
                image_path=path
            )
            db.session.add(lab_image)
            db.session.commit()

            flash("Image uploaded successfully.", "success")
            return redirect(url_for('lab_dashboard'))
        else:
            flash("Invalid image format.", "danger")

    return render_template('lab_dashboard.html', lab=lab, doctors=doctors, replies=replies)

@app.route('/patient_dashboard')
def patient_dashboard():
    if 'custom_id' not in session:
        return redirect(url_for('login_page'))

    patient_id = session['custom_id']
    patient = Patient.query.filter_by(custom_id=patient_id).first()
    doctors = Doctor.query.all()

    # ✅ Only fetch messages that contain a reply from doctor
    replies = PatientDoctorMessage.query.filter_by(patient_id=patient_id).filter(PatientDoctorMessage.reply_text.isnot(None)).order_by(PatientDoctorMessage.timestamp.desc()).all()

    return render_template('patient_dashboard.html', patient=patient, doctors=doctors, replies=replies)

@app.route('/reply_lab_message', methods=['POST'])
def reply_lab_message():
    if 'custom_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login_page'))

    doctor_id = session['custom_id']
    lab_id = request.form.get('lab_id')

    # Optional: Get reply_text = request.form.get('reply_text') — not stored

    # Delete all messages from this lab to this doctor
    LabDoctorMessage.query.filter_by(doctor_id=doctor_id, lab_id=lab_id).delete()
    db.session.commit()

    flash("Reply sent and messages cleared.", "success")
    return redirect(url_for('doctor_dashboard'))

@app.route('/reply_message', methods=['POST'])
def reply_message():
    if 'custom_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login_page'))

    doctor_id = session['custom_id']
    patient_id = request.form.get('patient_id')
    reply_text = request.form.get('reply_text')

    # ✅ Find the latest message from patient to doctor
    patient_msg = PatientDoctorMessage.query.filter_by(patient_id=patient_id, doctor_id=doctor_id).order_by(PatientDoctorMessage.timestamp.desc()).first()

    if patient_msg:
        patient_msg.reply_text = reply_text
        db.session.commit()
        flash("Reply sent successfully.", "success")
    else:
        flash("No original message found.", "danger")

    return redirect(url_for('doctor_dashboard'))
# DOCTOR DASHBOARD
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'custom_id' not in session:
        return redirect(url_for('login_page'))

    doctor_id = session['custom_id']
    doctor = Doctor.query.get(doctor_id)

    # Patient encrypted messages
    # Messages from patients
    messages = PatientDoctorMessage.query.filter_by(doctor_id=doctor_id).order_by(PatientDoctorMessage.timestamp.desc()).all()
    patient_messages = [msg for msg in messages if msg.patient_id and msg.encrypted_message]

    # Replies from doctor
    doctor_replies = PatientDoctorMessage.query.filter_by(doctor_id=doctor_id).order_by(PatientDoctorMessage.timestamp.desc()).all()
    for msg in messages:
        msg.decrypted_message = decrypt_message(msg.encrypted_message)
    doctor_sent_replies = [msg for msg in doctor_replies if msg.doctor_id == doctor_id and msg.patient_id]

    # Lab encrypted messages
    lab_messages = LabDoctorMessage.query.filter_by(doctor_id=doctor_id).order_by(LabDoctorMessage.timestamp.desc()).all()
    for msg in lab_messages:
        msg.decrypted_message = decrypt_message(msg.encrypted_message)

    # Patient images
    patient_images = PatientImageMessage.query.filter_by(doctor_id=doctor_id).order_by(PatientImageMessage.timestamp.desc()).all()

    # Lab images
    lab_images = LabImageMessage.query.filter_by(doctor_id=doctor_id).order_by(LabImageMessage.timestamp.desc()).all()

    return render_template(
        'doctor_dashboard.html',
        doctor=doctor,
        messages=messages,
        lab_messages=lab_messages,
        patient_images=patient_images,
        lab_images=lab_images
    )

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'custom_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login_page'))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    labs = Lab.query.all()
    hospitals = Hospital.query.all()
    admins = Admin.query.all()

    return render_template(
        'admin_dashboard.html',
        patients=patients,
        doctors=doctors,
        labs=labs,
        hospitals=hospitals,
        admins=admins
    )
@app.route('/hospital_dashboard')
def hospital_dashboard():
    if 'custom_id' not in session:
        return redirect(url_for('login_page'))

    # Fetch data from the database
    doctors = Doctor.query.all()
    labs = Lab.query.all()
    hospitals = Hospital.query.all()
    admins = Admin.query.all()

    return render_template('hospital_dashboard.html',
                           doctors=doctors,
                           labs=labs,
                           hospitals=hospitals,
                           admins=admins)

@app.route('/patient_details')
def patient_details():
    return render_template('patient_details.html')

@app.route('/hospital_office')
def hospital_office():
    return render_template('hospital_office.html')

@app.route('/upload_report')
def upload_report():
    return render_template('upload_report.html')

if __name__ == "__main__":
    app.run(debug=True)
