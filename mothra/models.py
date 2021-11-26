from mothra import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime

start = datetime(2021, 4, 13)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    roll = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(128))
    level = db.Column(db.Integer, default=0)
    upgrade_time = db.Column(db.DateTime)
    notif_count = db.Column(db.Integer, default=0)

    def __init__(self, roll, username, password, user_type):
        self.roll = roll
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_type = user_type
        self.upgrade_time = datetime.now()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.id}, {self.roll}, {self.username}"


class Attempts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    of = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stage = db.Column(db.Integer)
    atmpts = db.Column(db.Integer, default=1)

    def __init__(self):
        self.of = current_user.id
        self.stage = current_user.level + 1

    def __repr__(self):
        return f"{self.id},{self.of},{self.atmpts}"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stage = db.Column(db.Integer, nullable=False)
    ans = db.Column(db.String, nullable=False)
    sub = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    correct = db.Column(db.Integer)
    review = db.Column(db.String)

    usr = db.relationship("User", backref="by", lazy=True)

    def __init__(self, ans, sub, correct):
        self.by = current_user.id
        self.stage = current_user.level + 1
        self.ans = ans
        self.sub = sub
        self.time = datetime.now()
        self.correct = correct

    def __repr__(self):
        return (
            f"{self.id},{self.by},{self.stage}, {self.sub}, {self.time}, {self.correct}"
        )


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.Integer, nullable=False, unique=True)
    question = db.Column(db.String)
    ans = db.Column(db.String)
    picture = db.Column(db.String(100))

    def __init__(self, stage, question, ans, picture):
        self.stage = stage
        self.question = question
        self.ans = ans
        self.picture = picture

    def __repr__(self):
        return f"{self.id},{self.stage},{self.question},{self.ans}, {self.picture}"


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String, nullable=False)

    def __init__(self, uid, message):
        self.uid = uid
        self.message = message

    def __repr__(self):
        return f"{self.id},{self.uid},{self.message}"


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f"{self.id}, {self.message}"


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    uptime = db.Column(db.DateTime, nullable=False)

    def __init__(self, uid, level, uptime):
        self.uid = uid
        self.level = level
        self.uptime = uptime

    def __repr__(self):
        return f"{self.uid}, {self.level}, {self.uptime}"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feed = db.Column(db.String, nullable=False)

    def __init__(self, rating, feed):
        self.uid = current_user.id
        self.rating = int(rating)
        self.feed = feed

    def __repr__(self):
        return f"{self.uid}, {self.rating}, {self.feed}"
