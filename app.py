from flask import Flask, render_template, request, redirect
from model import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trekking_mgmnt.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role='admin').first()
    if admin is None:
        admin=User(user_email='admin@gmail.com',
                   user_password= 'admin123',
                   role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        user_email=request.form.get('user_email')
        user_password = request.form.get('user_password')
        user = User.query.filter_by(user_email=user_email, user_password=user_password).first()
        print(user)
        print(user.role)
        if user is not None:
            if user.role=='admin':
                treks=Trek.query.all()
                return render_template("admin_dashboard.html", treks=treks)
            if user.role=='trek_staff':
                return render_template('trek_staff_dashboard.html')
            if user.role=='user':
                return render_template('user_dashboard.html')
        else:
            return render_template('login.html')

@app.route('/add_trek', methods=['GET', 'POST'])
def add_trek():
    if request.method=='GET':
        return render_template("add_trek.html")
    if request.method=='POST':
        trek_name= request.form.get('trek_name')
        trek = Trek(trek_name=trek_name)
        db.session.add(trek)
        db.session.commit()
        treks=Trek.query.all()
        return render_template("admin_dashboard.html", treks=treks)

if __name__ == '__main__':
    app.run(debug=True)
