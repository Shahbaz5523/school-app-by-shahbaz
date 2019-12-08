from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import random
import string

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "userDatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Admin(db.Model):
    name = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(30), unique=False, nullable=False)


class Student(db.Model):
    name = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    cellNo = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)


class Teacher(db.Model):
    name = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    cellNo = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)


# db.create_all()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/addStaff', methods=['POST', 'GET'])
def addStaff():
    if request.method == "POST":
        admins = Admin().query.all()
        name = request.form['name']
        password = request.form['password']
        for myAdmin in admins:
            if name == myAdmin.name and password == myAdmin.password:
                return render_template('addStaff.html')
            else:
                return render_template('admin.html')

    return render_template('admin.html')


@app.route('/newUser', methods=['POST', 'GET'])
def newUser():
    if request.method == "POST":
        userName = request.form['name']
        userNumber = request.form['number']
        userType = request.form['userType']

        # radnomPasswod

        randomSource = string.ascii_letters + string.digits + string.punctuation
        password = random.choice(string.ascii_lowercase)
        password += random.choice(string.ascii_uppercase)
        password += random.choice(string.digits)
        password += random.choice(string.punctuation)

        for i in range(6):
            password += random.choice(randomSource)

        passwordList = list(password)
        random.SystemRandom().shuffle(passwordList)
        password = ''.join(passwordList)

        if userType == 'Student':
            newStudent = Student()
            newStudent.name = userName
            newStudent.password = password
            newStudent.cellNo = userNumber
            db.session.add(newStudent)
            db.session.commit()
            return render_template('staffinfo.html', user=newStudent)
        else:
            newTeacher = Teacher()
            newTeacher.name = userName
            newTeacher.password = password
            newTeacher.cellNo = userNumber
            db.session.add(newTeacher)
            db.session.commit()
            return render_template('staffinfo.html', user=newTeacher)


@app.route('/userlogin', methods=['POST', 'GET'])
def userLogin():
    return render_template('staffLogin.html')


@app.route('/userData', methods=['POST', 'GET'])
def userData():
    if request.method == "POST":
        userName = request.form['name']
        userType = request.form['userType']
        userPassword = request.form['password']
        if userType == 'Student':
            mystudents = Student().query.all()
            for student in mystudents:
                if userName == student.name and userPassword == student.password:
                    print("login")
                    targetStudent = Student().query.filter_by(name=userName).first()
                    return render_template('userData.html', user=targetStudent, utype=userType)
                else:
                    return render_template('staffLogin.html')
        else:
            myteachers = Teacher().query.all()
            for teacher in myteachers:
                if userName == teacher.name and userPassword == teacher.password:
                    targetTeacher = Teacher().query.filter_by(name=userName).first()
                    return render_template('userData.html', user=targetTeacher, utype=userType)
                else:
                    return render_template('staffLogin.html')


@app.route('/updateData', methods=['POST', 'GET'])
def updateData():
    if request.method == "POST":
        username = request.form['name']
        usernumber = request.form['number']
        userPassword = request.form['password']
        userType = request.form['userType']
        if userType == 'Student':
            targetStudent = Student().query.filter_by(name=username).first()
            targetStudent.name = username
            targetStudent.number = usernumber
            targetStudent.password = userPassword
            db.session.commit()
            return render_template('dataUpgrade.html')
        else:
            targetTeacher = Teacher().query.filter_by(name=username).first()
            targetTeacher.name = username
            targetTeacher.number = usernumber
            targetTeacher.password = userPassword
            db.session.commit()
            return render_template('dataUpgrade.html')

if __name__ == "__main__":
    app.run(debug=True)
