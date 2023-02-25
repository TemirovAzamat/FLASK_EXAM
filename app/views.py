from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from . import db
from .models import Position, Employee, User
from .forms import PositionForm, EmployeeForm, UserForm


def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


def position_create():
    title = 'Создание Позиции'
    form = PositionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            position = Position()
            form.populate_obj(position)
            db.session.add(position)
            db.session.commit()
            flash('Успешно сохранено', 'success')
            return redirect(url_for('index'))
    return render_template('standard_form.html', form=form, title=title)


def employee_create():
    title = 'Создание Сотрудника'
    form = EmployeeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = Employee()
            form.populate_obj(employee)
            db.session.add(employee)
            try:
                db.session.commit()
            except IntegrityError:
                flash('Такой сотрудник уже существует', 'danger')
                return render_template('standard_form.html', form=form, title=title)
            else:
                flash('Успешно сохранено', 'success')
                return redirect(url_for('index'))
    return render_template('standard_form.html', form=form, title=title)


@login_required
def employee_update(id):
    employee = Employee.query.get(id)
    form = EmployeeForm(obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            try:
                db.session.commit()
            except Exception as e:
                flash(f'Ошибка: {e}', 'danger')
            else:
                flash('Успешно обновлено', 'success')
                return redirect(url_for('index'))
    return render_template('standard_form.html', form=form)


@login_required
def employee_delete(id):
    employee = Employee.query.get(id)
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Успешно удалено', 'success')
        return redirect(url_for('index'))
    return render_template('confirm_delete.html', employee=employee)


def register():
    title = 'Регистрация!'
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                flash('Такой пользователь уже есть', 'danger')
            else:
                flash('Вы успешно зарегистрировались!', 'success')
                return redirect(url_for('login'))
    return render_template('user_form.html', form=form, title=title)


def login():
    title = 'Авторизация!'
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли', 'success')
                return redirect(url_for('index'))
    return render_template('user_form.html', form=form, title=title)


def logout():
    logout_user()
    return redirect(url_for('login'))
