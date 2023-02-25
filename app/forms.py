from flask_wtf import FlaskForm
import wtforms as wf

from . import app
from .models import Position


class PositionForm(FlaskForm):
    name = wf.StringField(label='Должность', validators=[
        wf.validators.DataRequired()
    ])
    department = wf.StringField(label='Отдел')
    wage = wf.IntegerField(label='Заработная плата', validators=[
        wf.validators.DataRequired()
    ])

    def validate_wage(self, field):
        if field.data < 0:
            raise wf.validators.ValidationError('Меньше 0 не бывает')


def get_positions():
    with app.app_context():
        positions = Position.query.all()
        choices = []
        for position in positions:
            choices.append((position.id, position.name))
        return choices


class EmployeeForm(FlaskForm):
    name = wf.StringField(label='Ваше имя', validators=[
        wf.validators.DataRequired()
    ])
    inn = wf.StringField(label='Ваш ИНН', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=14, max=14)
    ])
    position_id = wf.SelectField(label='Ваша позиция', choices=[], validators=[
        wf.validators.DataRequired()
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position_id.choices = get_positions()

    def validate_inn(self, field):
        if field.data[0] != '1' and field.data[0] != '2':
            raise wf.validators.ValidationError('ИНН должен начинаться с 1 или 2')


class UserForm(FlaskForm):
    username = wf.StringField(label='Логин пользователя', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=8, max=24)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate_password(self, field):
        if field.data.isdigit() or field.data.isalpha():
            raise wf.validators.ValidationError('Пароль должен содержать числа и буквы')
