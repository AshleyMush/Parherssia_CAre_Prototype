from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length, ValidationError, InputRequired
import re
from flask import flash


class CallbackForm(FlaskForm):
    callback_name = StringField('Name', validators=[DataRequired(), Length(max=64)],
                                render_kw={"placeholder": "Name", "class": "form-control"})
    callback_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)],
                                  render_kw={"placeholder": "Contact Number", "class": "form-control"})
    callback_message = TextAreaField('Message', validators=[DataRequired()],
                                     render_kw={"placeholder": "Reason for call back"})

    def validate_callback_number(self, field):
        if not re.match(r'^\+?1?\d{9,15}$', field.data):
            raise ValidationError("Invalid contact number. Enter a valid number with 9 to 15 digits.")

    submit = SubmitField('Request CallBack', render_kw={"class": "btn btn-primary call-back-btn"})


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "Name", "id": "name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email", "id": "email"})
    subject = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Subject", "id": "subject"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"id": "message", "placeholder": "Enter your message", "rows": 6})
    submit = SubmitField('Send Message', render_kw={'id':'contact_submit_btn'})


