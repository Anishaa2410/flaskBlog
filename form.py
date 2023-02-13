from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flaskblog.model import User
from flask_wtf.file import FileAllowed, FileField


class RegisterationForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), length(min=2, max=10)])
    email= StringField('Email', validators=[DataRequired(), Email()])
    password= StringField('Password', validators=[DataRequired()])
    confirm_password= StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    # to make sure different username is used, we'll use function for validation
    def val_username(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username taken!")

    def val_mail(self, mail):
        user= User.query.filter_by(mail = email.data).first()
        if user:
            raise ValidationError("mail taken!")


class LoginForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    password= StringField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember me?')
    submit=SubmitField('Login')


class AccountUpdateForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), length(min=2, max=10)])
    email= StringField('Email', validators=[DataRequired(), Email()])
    picture= FileField('Update Profile Picture' , validators=[FileAllowed(['jpg' , 'png'])])
    submit=SubmitField('Update')

    # to make sure different username is used, we'll use function for validation
    def val_username(self, username):
        if username.data != current_user.username :
            user= User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username taken!")
        if User.query.filter_by(username=username.data).first() and username.data != current_user.email:
          raise ValidationError('Email has been already been registered.')
    def val_mail(self, mail):
        if mail.data != current_user.email :
            user= User.query.filter_by(mail = email.data).first()
            if user:
                raise ValidationError("mail taken!")

class PostForm(FlaskForm):
    title = StringField('Enter title',validators=[DataRequired(), length(min=2, max=20)] )
    content = TextAreaField('Enter Content',validators=[DataRequired(), length(min=5)] )
    submit=SubmitField('Add Post')
