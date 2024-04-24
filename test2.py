from flask import Flask, request,render_template, redirect,session,flash,jsonify,json
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
import redis
import bcrypt
import re

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db_username = 'postgres'
db_password = 'Musk%401702'
db_host = 'localhost'
db_port = '5432'
db_name = 'Astrotaal'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
db = SQLAlchemy(app)
app.secret_key = 'secret_key_astrotaal'

# Configure Redis for Flask-Session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')


# Set session expiry time (in seconds)
app.config['PERMANENT_SESSION_LIFETIME'] = 300 # 1 min expiry time

# Initialize Flask-Session
Session(app)

# function for validating email
def validate_email(email):
    """
    Validate the format of an email address using a regular expression.
    """
    # Regular expression pattern for validating email addresses
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    dob = db.Column(db.Date)
    time_of_birth = db.Column(db.String(10))
    location_of_birth = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    marital_status = db.Column(db.String(20))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email

        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/check_redis')
def check_redis():
    try:
        # Attempt to connect to Redis
        redis_client = redis.StrictRedis(host='localhost', port=6379)
        redis_client.ping()
        return jsonify({'status': 'success', 'message': 'Redis is running and accessible.'}), 200
    except redis.ConnectionError:
        return jsonify({'status': 'error', 'message': 'Could not connect to Redis. Make sure it is running.'}), 500

# Check if session data has expired
def is_session_expired(session_key):
    redis_client = redis.StrictRedis(host='localhost', port=6379)
    # Check the TTL (time to live) of the session key
    ttl = redis_client.ttl(session_key)
    if ttl == -2:
        return True  # Session data does not exist or has expired
    elif ttl == -1:
        return False  # Session data exists and has no expiration
    else:
        return False  # Session data exists and has not expired yet



@app.route('/')
def index():
    session_key = 'session:' + session.sid
    if is_session_expired(session_key):
        return 'Session has expired'
    else:
        return 'Session is still active'
    
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if name =="" or email=="" or password=="":
            flash('Please fill all the fields','danger')
            return redirect('/register')
        else:
            if validate_email(email):
                user = User.query.filter_by(email=email).first()
                if user:
                    flash('Email already Exist','danger')
                    return redirect('/register')
                else:
                    new_user = User(name=name,email=email,password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    flash ('Email registered successfully','success')
                    return redirect('/login')
            else:
                flash ('Invalid email address','danger')
            
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            session['user_id'] = user.id
            return redirect('/profile/update')
        else:
            flash('Invalid Email and Password','danger')
            return redirect('/login')
    return render_template('login.html')


@app.route('/profile/update',methods=['GET','POST'])
def profile():
    if not session.get('user_id'):
        return ('User not logged in')
    if session.get('user_id'):
        id=session.get('user_id')
    users=User.query.get(id)
    if request.method == 'POST':
        # get all input field name
        name=request.form.get('name')
        dob=request.form.get('dob')
        time_of_birth=request.form.get('time_of_birth')
        location_of_birth=request.form.get('location_of_birth')
        phone_number=request.form.get('phone_number')
        email=request.form.get('email')
        marital_status=request.form.get('marital_status')
    
        if name =="" or dob=="" or email=="" or time_of_birth=="" or location_of_birth=="" or phone_number=="" or marital_status=="":
            return jsonify({'message': 'Please fill all the fields'}), 400
        else:
            # 2session['email']=email
            if validate_email(email):
                try:
                    datetime.strptime(dob, '%Y-%m-%d')
                    User.query.filter_by(id=id).update(dict(email=email,name=name,dob=dob,time_of_birth=time_of_birth,location_of_birth=location_of_birth,phone_number=phone_number,marital_status=marital_status))
                    db.session.commit()
                    flash('Profile updated Successfully','success')
                    return redirect('/login')
                except ValueError:
                    return jsonify({'message': 'Invalid date format. Date should be in YYYY-MM-DD format.'}), 400
            else:
                flash('Invalid email address','danger')
        return redirect('/profile/update')     
    else:
        return render_template('/profile.html',title="Update Profile",users=users)
@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)