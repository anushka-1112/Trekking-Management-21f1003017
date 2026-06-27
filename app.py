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
                   user_name='Admin',
                   role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/admin_dashboard')
def admin_dashboard():
    treks=Trek.query.all()
    users = User.query.all()
    return render_template("admin_dashboard.html", treks=treks, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        user_email=request.form.get('user_email')
        user_password = request.form.get('user_password')
        user = User.query.filter_by(user_email=user_email, user_password=user_password).first()
        if user is not None:
            if user.role=='admin':
                treks=Trek.query.all()
                return redirect('/admin_dashboard')
            if user.role=='trek_staff' and user.blacklisted == False:
                return render_template('trek_staff_dashboard.html', approved_status = user.approved)
            if user.role=='user' and user.blacklisted==False:
                return render_template('user_dashboard.html')
        else:
            return render_template('login.html')

@app.route('/add_trek', methods=['GET', 'POST'])
@app.route('/add_trek/<int:trek_id>', methods=['GET', 'PATCH', 'DELETE'])
def add_trek(trek_id=None):
    method = request.environ.get('REQUEST_METHOD', request.method)
    if method=='GET':
        if not trek_id:
            trek_id = request.args.get('trek_id')
        trek = None
        if trek_id:
            print(trek_id)
            trek = db.session.get(Trek, trek_id)
        return render_template("add_trek.html", trek=trek)
    

    if method=='POST':
        trek_name= request.form.get('trek_name')
        trek = Trek(trek_name=trek_name)
        db.session.add(trek)
        db.session.commit()
        treks=Trek.query.all()
        return render_template("admin_dashboard.html", treks=treks)

    if method == 'PATCH':
        trek_id = request.form.get('trek_id')
        trek_name = request.form.get('trek_name_upd')
        trek = db.session.get(Trek, trek_id)
        trek.trek_name=trek_name
        db.session.commit()
        treks=Trek.query.all()
        return render_template("admin_dashboard.html", treks=treks)
    
    if method=='DELETE':
        trek_id = request.form.get('trek_id')
        trek = db.session.get(Trek, trek_id)
        db.session.delete(trek)
        db.session.commit()
        treks=Trek.query.all()
        return render_template("admin_dashboard.html", treks=treks)


@app.before_request
def before_request():
    if request.method=='POST' and '_method' in request.form:
        method = request.form.get('_method').upper()
        if method in ['PATCH', 'DELETE', 'PUT']:
            request.environ['REQUEST_METHOD']=method

@app.route('/search_trek', methods=['GET', 'POST'])
def search_treks():
    if request.method=='GET':
        treks=Trek.query.all()
        return render_template("admin_dashboard.html", treks=treks)
    if request.method=='POST':
        search_string = request.form.get('s_trek', '').strip() #--ek--
        searched_treks=[]
        search_performed=True
        if search_string:
            searched_treks = Trek.query.filter(Trek.trek_name.ilike(f'%{search_string}%')).all()
        treks=Trek.query.all()
        return render_template("admin_dashboard.html", treks=treks,
                               search_performed=search_performed,
                               searched_data = searched_treks)   

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method=='POST':
        email=request.form.get("user_email")
        password=request.form.get("user_password")
        name = request.form.get("user_name")
        role = request.form.get("role")
        if role in ('user', 'trek_staff'):
            new_user = User(user_name=name,
                            user_email=email,
                            user_password=password,
                            role=role)
            db.session.add(new_user)
            db.session.commit()
        return redirect('/login')

@app.route('/staff_approve/<int:user_id>')
def approve_staff_profile(user_id):
    user = db.session.get(User, user_id)
    user.approved=True
    db.session.commit()
    return redirect('/admin_dashboard')

@app.route('/blacklist/<int:user_id>')
def blacklist_user(user_id):
    if user_id:
        user=db.session.get(User, user_id)
        if user and user.role in ('trek_staff', 'user'):
            user.blacklisted=True
            db.session.commit()
    return redirect('/admin_dashboard')

@app.route('/unblacklist/<int:user_id>')
def unblacklist_user(user_id):
    if user_id:
        user=db.session.get(User, user_id)
        if user and user.role in ('trek_staff', 'user'):
            user.blacklisted=False
            db.session.commit()
    return redirect('/admin_dashboard')


# @app.route('/update_trek/<int:trek_id>', methods=['GET', 'POST'])
# def update_trek(trek_id):
#     if request.method=='GET':
#         trek = Trek.query.get(trek_id=trek_id)
#         return render_template("edit_trek.html", trek=trek)
#     if request.method=='POST':
#         trek_name= request.form.get('trek_name')
#         # trek = Trek.query.get(trek_id=trek_id)
#         # trek.trek_name=trek_name
#         trek = Trek.query.filter_by(trek_id=trek_id).update(dict(trek_name=trek_name))
#         db.session.commit()
#         treks=Trek.query.all()
#         return render_template("admin_dashboard.html", treks=treks)


if __name__ == '__main__':
    app.run(debug=True)
