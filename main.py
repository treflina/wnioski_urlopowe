from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.orm import relationship
from functools import wraps
from forms import EditEmployeeForm, SickLeaveForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_mail import Mail, Message
import re

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.environ.get("MYSECRET_KEY")
app.config['MAIL_SERVER']=os.environ.get("MYMAIL_SERVER")
app.config['MAIL_USERNAME'] = os.environ.get("MYMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MYMAIL_PASSWORD")

app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True





ADMIN_LOGIN=["wynik", "kampa"] # Admin_login also hardcoded in header.html

login_manager = LoginManager()
login_manager.init_app(app)

uri = os.getenv("DATABASE_URL", 'sqlite:///wnioski1.db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI']=uri

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wnioski1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(session_options={"autoflush": False})
db = SQLAlchemy(app)
Bootstrap(app)
mail=Mail(app)
admin=Admin(app)
migrate = Migrate(app, db)


class Employee(UserMixin, db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    login = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(100))
    position = db.Column(db.String(50), unique=False)
    position_info=db.Column(db.String(20))
    work_place=db.Column(db.String)
    is_manager = db.Column(db.String(3), nullable=False)
    is_topmanager = db.Column(db.String(3), nullable=False)
    work_time = db.Column(db.Float, unique=False, nullable=False)
    email=db.Column(db.String)
    days_off = db.Column(db.Integer, nullable=False)
    annual_days_off=db.Column(db.Integer)
    contract_end = db.Column(db.String)
    requests = relationship("Request", back_populates="author")
    sickleaves = relationship("SickLeave", back_populates="person")
    manager_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    manager = relationship("Employee", backref='subordinates', remote_side="Employee.id")
    today_note=db.Column(db.String(20))
    additional_info=db.Column(db.String)

    def __repr__(self):
        return '<Employee %r>' %(self.name)

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.login in ADMIN_LOGIN:
            return True


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    author = relationship("Employee", back_populates="requests")
    type = db.Column(db.String(250), nullable=False)
    work_date = db.Column(db.String(250))
    send_date = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.String(250), nullable=False)
    end_date = db.Column(db.String(250))
    days = db.Column(db.Integer)
    status = db.Column(db.String(15))
    substitute = db.Column(db.String(50), nullable=True)
    send_to_person = db.Column(db.String(50))
    signed_by = db.Column(db.String(50))
    def __repr__(self):
        return '<Request %r>' %(self.id)

class SickLeave(db.Model):
    __tablename__ = "sickleaves"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    person = relationship("Employee", back_populates="sickleaves")
    doc_number = db.Column(db.String(250))
    type = db.Column(db.String(250), nullable=False)
    issue_date = db.Column(db.String(250))
    start_date = db.Column(db.String(250), nullable=False)
    end_date = db.Column(db.String(250), nullable=False)
    days = db.Column(db.Integer)
    def __repr__(self):
        return '<SickLeave %r>' %(self.id)


# To uncomment during the first use to create director/admin, then add the rest of the users using /admin_site

# db.create_all()
#
# # Create first employee:
# first_employee=Employee(name="Kampa Anna", login="kampa", password=generate_password_hash(
#                 "1111",
#                 method='pbkdf2:sha256',
#                 salt_length=8), position="dyrektor", days_off=26, is_manager="TAK", is_topmanager="TAK", work_time=1.0)
# db.session.add(first_employee)
# db.session.commit()


@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_logins=["treflina", "kampa"]
        if current_user.login not in admin_logins:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        employee_to_check = Employee.query.filter_by(login=login).first()
        if not employee_to_check:
            flash("Nieprawidłowa nazwa użytkownika. Spróbuj ponownie")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(employee_to_check.password, password):
            flash('Nieprawidłowe hasło. Spróbuj ponownie.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(employee_to_check)
            return redirect(url_for("main"))
    return render_template("login.html")



@app.route("/change_password", methods=["POST", "GET"])
def change_password():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["old_password"]
        employee_to_change = Employee.query.filter_by(login=login).first()
        if not employee_to_change:
            flash("Nieprawidłowa nazwa użytkownika. Spróbuj jeszcze raz.")
            return redirect(url_for('change_password'))
        # Password incorrect
        elif not check_password_hash(employee_to_change.password, password):
            flash('Nieprawidłowe dotychczasowe hasło. Spróbuj jeszcze raz')
            return redirect(url_for('change_password'))
        # Login exists and password correct
        else:
            hashed_and_salted_password = generate_password_hash(
                request.form["up"],
                method='pbkdf2:sha256',
                salt_length=8
            )
            employee_to_change.password = hashed_and_salted_password

            db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/", methods=["GET"])
def main():
    if current_user.is_authenticated:
        name_split=current_user.name.split(" ")
        name_reverse=name_split[1]+" "+name_split[0]

        top_management = db.session.query(Employee).filter(Employee.is_topmanager=="TAK").all()

        employee_to_search = Employee.query.get(current_user.id)
        employees_requests_received = db.session.query(Request).filter(
            Request.send_to_person == employee_to_search.name).filter(Request.status == "oczekujący")
        request_list = len(employees_requests_received.all())

        today = date.today().strftime("%d/%m/%y")
        today_sickleaves = db.session.query(SickLeave).filter(SickLeave.start_date >= today).filter(
            SickLeave.end_date <= today).all()
        today_requests = db.session.query(Request).filter(Request.start_date >= today).filter(Request.end_date <= today).all()
        print(today_requests)
        print(today_sickleaves)
        if current_user.position=="dyrektor":
            return redirect(url_for('employees_list', request_list=request_list, today_sickleaves=today_sickleaves, today_requests=today_requests))
        else:
            return render_template("main.html", name_reverse=name_reverse, top_management=top_management, request_list=request_list)
    return redirect(url_for('login'))



@app.route("/my_requests")
@login_required
def my_requests():
    user_requests_holiday = db.session.query(Request).filter(Request.author_id == current_user.id).filter(
        Request.type == "W").order_by(desc(Request.send_date)).all()

    user_requests_others = db.session.query(Request).filter(
        (Request.type == 'WS') | (Request.type == 'WN') | (Request.type == "DW")).filter(
        Request.author_id == current_user.id).order_by(desc(Request.send_date)).all()
    return render_template("my_requests.html", user_requests_holiday=user_requests_holiday,user_requests_others=user_requests_others)


@app.route("/employees_requests")
@login_required
def employees_requests():
    employee_to_search = Employee.query.get(current_user.id)

    employees_requests_received=db.session.query(Request).filter(
        Request.send_to_person == employee_to_search.name).filter(Request.status=="oczekujący")
    employees_requests_others = db.session.query(Request).filter(
        (Request.type == 'WS') | (Request.type == 'WN') | (Request.type == "DW")).order_by(desc(Request.send_date)).all()
    employees_requests_holiday = db.session.query(Request).filter(Request.type == "W").order_by(desc(Request.send_date)).all()
    request_list=len(employees_requests_received.all())
    return render_template("employees_requests.html",  employees_requests_received= employees_requests_received, employees_requests_holiday=employees_requests_holiday,
                           employees_requests_others=employees_requests_others, request_list=request_list)

@app.route("/sickleaves")
@login_required
def sickleaves():
    sickleaves = SickLeave.query.order_by(SickLeave.issue_date).all()
    return render_template("sickleaves.html", sickleaves=sickleaves)

@app.route("/admin_site", methods=["POST", "GET"])
@admin_only
def admin_site():
    all_employees = Employee.query.order_by(Employee.name).all()
    return render_template("admin_site.html", all_employees=all_employees)

@app.route("/employees_list")
@login_required
def employees_list():
    all_employees = Employee.query.order_by(Employee.name).all()

    employee_to_search = Employee.query.get(current_user.id)
    employees_requests_received = db.session.query(Request).filter(
        Request.send_to_person == employee_to_search.name).filter(Request.status == "oczekujący")
    request_list = len(employees_requests_received.all())

    today=date.today().strftime("%d/%m/%y")
    today_requests=db.session.query(Request).filter(Request.start_date <= today).filter(Request.end_date >= today)
    today_sickleaves=db.session.query(SickLeave).filter(SickLeave.start_date <= today).filter(SickLeave.end_date >= today)

    # for employee in all_employees:
    #     todays=db.session.query(SickLeave).filter(SickLeave.start_date <= today).filter(SickLeave.end_date >= today).filter(SickLeave.person_id==employee.id).all()
    #     todayr=db.session.query(Request).filter(Request.start_date <= today).filter(Request.end_date >= today).filter(Request.author_id==employee.id).all()
    #
    #     if len(todays)!=0:
    #         for ts in todays:
    #             temporary_lista=[]
    #             temporary_lista.append(ts.type)
    #             employee.today_note = temporary_lista[0]
    #
    #     elif len(todayr)!=0:
    #         for tr in todayr:
    #             temporary_list2 = []
    #             temporary_list2.append(tr.type)
    #             list.append(temporary_list2[0])
    #             employee.today_note=temporary_list2[0]
    #     else:
    #         employee.today_note = "✓"
    return render_template("employees_list.html", list=list, request_list=request_list, today_sickleaves=today_sickleaves, today_requests= today_requests, all_employees=all_employees)


@app.route("/send_request", methods=["POST", "GET"])
@login_required
def send_request():
    if request.method == "POST":
        try:
            substitute=request.form["substitute"]
        except:
            substitute=""
        if request.form["type"]=="W":
            work_date=""
        else:
            work_date=request.form["work_date"]
        new_request = Request(type=request.form["type"],
                              author=current_user,
                              work_date=work_date,
                              start_date=request.form["startdate"],
                              end_date=request.form["enddate"],
                              substitute=substitute,
                              days=request.form["days_count"],
                              status="oczekujący",
                              send_date=date.today().strftime("%d/%m/%y"),
                              send_to_person=request.form["person_to_send"])
        if request.form["type"] == "W":
            employee_to_update = Employee.query.get(current_user.id)
            new_days_off_count = employee_to_update.days_off - int(request.form["days_count"])
            employee_to_update.days_off = new_days_off_count
        db.session.add(new_request)
        db.session.commit()
        flash('Twój wniosek został pomyślnie złożony.')
    return redirect(url_for("main"))


@app.route("/accept_request/<int:request_id>/<int:manager_id>")
@login_required
def accept_request(request_id, manager_id):
    request_to_accept = Request.query.get(request_id)
    request_to_accept.status = "zaakceptowany"
    person_who_signed = Employee.query.get(manager_id).name
    request_to_accept.signed_by = person_who_signed
    db.session.commit()
    return redirect(url_for('main'))


@app.route("/reject_request/<int:request_id>/<int:manager_id>")
@login_required
def reject_request(request_id, manager_id):
    request_to_reject = Request.query.get(request_id)
    request_to_reject.status = "odrzucony"
    person_who_signed = Employee.query.get(manager_id).name
    request_to_reject.signed_by = person_who_signed
    if request_to_reject.type == "W":
        employee_to_update = Employee.query.get(request_to_reject.author.id)
        new_days_off_count = employee_to_update.days_off + request_to_reject.days
        employee_to_update.days_off = new_days_off_count
    db.session.commit()
    return redirect(url_for('employees_requests'))

@app.route("/withdraw_request/<int:request_id>")
@login_required
def withdraw_request(request_id):
    request_to_withdraw=Request.query.get(request_id)
    if request_to_withdraw.type == "W":
        employee_to_update = Employee.query.get(request_to_withdraw.author.id)
        new_days_off_count = employee_to_update.days_off + request_to_withdraw.days
        employee_to_update.days_off = new_days_off_count
    db.session.delete(request_to_withdraw)
    db.session.commit()
    return redirect(url_for('my_requests'))


@app.route("/add", methods=["POST", "GET"])
@admin_only
def add_employee():
    is_edit = False
    form = EditEmployeeForm()
    form.manager.choices = [(g.id, g.name) for g in Employee.query.filter_by(is_manager="TAK").order_by('name').all()]
    if request.method == "POST":
        try:
            work_time = request.form["work_time"].replace(",", ".")
        except:
            work_time = request.form["work_time"]
        hash_and_salted_password = generate_password_hash(
            request.form["password"],
            method='pbkdf2:sha256',
            salt_length=8
        )
        if Employee.query.filter_by(login=request.form["login"]).first():
            # User already exists
            flash("Ta nazwa użytkownika jest już w bazie. Podaj inny login.")
            return redirect(url_for('add_employee'))
        else:

            employee_to_relate = Employee.query.get(request.form["manager"])
            manager_id = employee_to_relate.id

            new_employee = Employee(name=request.form["name"], login=request.form["login"], email=request.form["email"],
                                    password=hash_and_salted_password, days_off=request.form["days_off"],
                                    work_time=work_time, work_place=request.form["work_place"],
                                    position=request.form["position"], position_info=request.form["position_info"], is_manager=request.form["is_manager"],
                                    is_topmanager=request.form["is_topmanager"],contract_end=request.form["contract_end"], manager_id=manager_id, additional_info=request.form["additional_info"])
            db.session.add(new_employee)
            db.session.commit()
            all_employees = db.session.query(Employee).all()
            return redirect(url_for('admin_site', all_employees=all_employees))
    return render_template("edit.html", is_edit=is_edit, form=form)

@app.route("/add_sickleave", methods=["POST", "GET"])
@admin_only
def add_sickleave():
    form = SickLeaveForm()

    if form.validate_on_submit():
        sick_employee=Employee.query.filter_by(name=form.name.data).first()
        if not sick_employee:
            flash('Nie znaleziono podanego pracownika w bazie. Sprawdź pisownię.')
        else:
            new_sickleave=SickLeave(person_id=sick_employee.id, issue_date=request.form["issue_date"], start_date=request.form["start_date"], end_date=request.form["end_date"], doc_number=request.form["doc_number"], type=request.form["type"], days=request.form["days"])
            director=Employee.query.filter_by(position="dyrektor").first()
            try:
                msg = Message(f"chorobowe {sick_employee.name}, ({request.form['start_date']}- {request.form['end_date']})", sender='treflina@yahoo.com', recipients=[director.email])
                msg.body = f"Pani Dyrektor,\r\n {sick_employee.name} przebywa na zwolnieniu lekarskim ({request.form['type']}) w dniach {request.form['start_date']} - {request.form['end_date']}.\r\n \r\nWiadomość wygenerowana automatycznie."
                mail.send(msg)
            except:
                flash("Nie udało się wysłać maila z informacją o zwolnieniu do dyrektora. Sprawdź ustawienia.")
            db.session.add(new_sickleave)
            db.session.commit()
            sickleaves = SickLeave.query.order_by(SickLeave.issue_date).all()
            return redirect(url_for('sickleaves', sickleaves=sickleaves))
    return render_template("add_sickleave.html", form=form)


@app.route("/edit/<int:employee_id>", methods=["POST", "GET"])
@admin_only
def edit_employee(employee_id):
    employee = Employee.query.get(employee_id)
    is_edit = True
    form = EditEmployeeForm(
        name=employee.name,
        login=employee.login,
        position=employee.position,
        position_info=employee.position_info,
        work_place=employee.work_place,
        work_time=employee.work_time,
        days_off=employee.days_off,
        annual_days_off=employee.annual_days_off,
        contract_end=employee.contract_end,
        is_manager=employee.is_manager,
        is_topmanager=employee.is_topmanager,
        email=employee.email,
        additional_info=employee.additional_info
    )
    try:
        form.manager.choices = [(employee.manager.id, employee.manager.name)] + [(g.id, g.name) for g in
                                                                                 Employee.query.filter_by(
                                                                                     is_manager="TAK").order_by(
                                                                                     'name').all()]
    except:
        form.manager.choices = [(g.id, g.name) for g in
                                Employee.query.filter_by(is_manager="TAK").order_by('name').all()]
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.login = form.login.data
        employee.email=form.email.data
        employee.position = form.position.data
        employee.position_info=form.position_info.data
        employee.work_place=form.work_place.data
        employee.work_time = form.work_time.data
        employee.days_off = form.days_off.data
        employee.annual_days_off=form.annual_days_off.data
        employee.is_manager = form.is_manager.data
        employee.is_topmanager=form.is_topmanager.data
        if form.position.data!="dyrektor":
            employee_to_relate = Employee.query.get(request.form["manager"])
            employee.manager_id = employee_to_relate.id
        employee.contract_end = form.contract_end.data
        employee.additional_info=form.additional_info.data
        db.session.commit()
        all_employees = db.session.query(Employee).all()
        return redirect(url_for("admin_site", all_employees=all_employees))

    return render_template('edit.html', form=form, is_edit=is_edit)


@app.route("/delete/<int:employee_id>")
@admin_only
def delete_employee(employee_id):
    employee_to_delete = Employee.query.get(employee_id)
    db.session.delete(employee_to_delete)
    db.session.commit()
    return redirect(url_for('admin_site'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

admin.add_view(MyModelView(Employee, db.session))
admin.add_view(MyModelView(Request, db.session))
admin.add_view(MyModelView(SickLeave, db.session))

if __name__ == "__main__":
    app.run(debug=True)
