from flask_wtf import FlaskForm
from wtforms import validators,ValidationError
from wtforms import (StringField,SubmitField,PasswordField,
BooleanField,TextAreaField,FileField)

from webblog.Models import User

from webblog import bcrypt


class Registerform(FlaskForm):
    
    username=StringField('Username',
    validators=[validators.DataRequired(),validators.Length(min=8)])

    email=StringField('Email',
    validators=[validators.DataRequired(),validators.Email()])

    password=PasswordField('Create Password',
    validators=[validators.DataRequired(),validators.Length(min=8),validators.Regexp('[@#$%^&*]')])

    conform_password=PasswordField('Conform Password',
    validators=[validators.DataRequired(),validators.EqualTo('password')])

    submit=SubmitField('Register')


    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken!')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken!\nTry another one')    





class LoginForm(FlaskForm):
    email=StringField('Email',validators=[validators.Email(),validators.Required()])

    password=PasswordField('Password',validators=[validators.DataRequired()])

    remember=BooleanField('Remember Me')

    login=SubmitField('Login')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email not found!')

      


class AddPost(FlaskForm):
    content=TextAreaField('Content')
    image=FileField('Image')

    add=SubmitField('Post')
    

class UpdatePost(FlaskForm):
    content=TextAreaField('Content')
    image=FileField('Image')
    update=SubmitField('Update')

