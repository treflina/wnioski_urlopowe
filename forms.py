from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, URL

class EditEmployeeForm(FlaskForm):
    name = StringField("Nazwisko i imię:", validators=[DataRequired()])

    login = StringField("Nazwa użytkownika (login):", validators=[DataRequired()])
    password=StringField("Hasło startowe:")
    position=StringField("Stanowisko:", validators=[DataRequired()])
    position_info=StringField('Dopisek dla rozróżnienia osoby przy dwóch umowach np. "sprz.":')
    manager=SelectField("Bezpośredni przełożony:",choices=[("Kowalska Anna","Kowalska Anna")])
    is_manager=RadioField("Kieruje pracownikami:", choices=[('TAK','TAK'),('NIE','NIE')], validators=[DataRequired()])
    is_topmanager = RadioField("Wykonuje zadania dyrektora:", choices=[('TAK', 'TAK'), ('NIE', 'NIE')],
                            validators=[DataRequired()])
    work_place=StringField("Placówka/Dział:")
    work_time=FloatField("Wymiar etatu (wpisz liczbowo):", validators=[DataRequired()])
    contract_end=StringField("Umowa do:")
    email=StringField("Email:")
    days_off=IntegerField("Obecna liczba dni urlopu:", validators=[DataRequired()])
    annual_days_off=IntegerField("Roczny wymiar urlopu:")
    additional_info = StringField("Uwagi:")
    submit = SubmitField("Zatwierdź")


class SickLeaveForm(FlaskForm):
    name=StringField("Nazwisko i imię:", validators=[DataRequired()])
    doc_number = StringField("Numer dokumentu:")
    issue_date = StringField("Data wystawienia (DD/MM/YY):")
    type = RadioField("Rodzaj:", choices=[('choroba', 'choroba'), ('opieka', 'opieka')],
                            validators=[DataRequired()])
    start_date = StringField("Od (DD/MM/YY):", validators=[DataRequired()])
    end_date = StringField("Do (DD/MM/YY):", validators=[DataRequired()])
    days = StringField("Liczba dni")
    submit = SubmitField("Zatwierdź")

class ReportForm(FlaskForm):
    person=SelectField("Dla:", choices=[("Kowalska Anna","Kowalska Anna")], validators=[DataRequired()])
    type = SelectField ("Rodzaj:", choices = [("o urlop wypoczynkowy", "urlop wypoczynkowy"), ("o dni wolne", "pozostałe (WS, WN, WŚ)")])
    start_date = StringField ("Od (dd/mm/yy):", validators=[DataRequired()])
    end_date = StringField("Do (dd/mm/yy):", validators=[DataRequired()])
    submit = SubmitField("Generuj pdf")
