from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    RadioField,
    IntegerField,
    TextAreaField,
    HiddenField,
)
from wtforms.validators import DataRequired, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DecimalRangeField
from flask_wtf.file import FileField, FileAllowed
from mothra.models import User, Stage


class LoginForm(FlaskForm):
    roll = StringField("Roll Number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    roll = IntegerField("Roll Number", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("pass_confirm", message="Passwords must Match!"),
        ],
    )
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_roll(self, roll):
        if User.query.filter_by(roll=self.roll.data).first():
            raise ValidationError("Roll Number already registered!")

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username already registered!")


class StageFillingForm(FlaskForm):
    stage = IntegerField("Stage", validators=[DataRequired()])
    question = StringField("Question", validators=[DataRequired()])
    ans = StringField("Answer", validators=[DataRequired()])
    picture = FileField(
        "Upload Image", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    submit = SubmitField("Submit")

    def validate_stage(self, stage):
        if Stage.query.filter_by(stage=self.stage.data).first():
            raise ValidationError("Stage already registered!")


class SubmissionForm(FlaskForm):
    ans = StringField("Answer", validators=[DataRequired()])
    sub = TextAreaField("Explanation", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    review = RadioField("Review", choices=["Reject", "Accept"])
    submission_id = HiddenField("submission_id")
    submit = SubmitField("Submit")


class AnnounceForm(FlaskForm):
    message = StringField("Announcement", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NotifForm(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired()])
    message = StringField("Notification", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FeedbackForm(FlaskForm):
    rating = DecimalRangeField("Rating", validators=[DataRequired()], default=50)
    feed = TextAreaField("Feedback", validators=[DataRequired()])
    submit = SubmitField("Submit")
