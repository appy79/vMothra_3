from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user
from mothra import db
from mothra.models import (
    User,
    Submission,
    Stage,
    Notification,
    Announcement,
    Stats,
    Feedback,
)
from mothra.forms import StageFillingForm, ReviewForm, AnnounceForm, NotifForm
from mothra.views import classify
from datetime import datetime
from mothra.godzilla.picture_handler import add_challenge_pic


godzilla = Blueprint("godzilla", __name__)


def godzilla_required(function):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_type == "Godzilla":
            return function()
        else:
            return abort(403)

    wrapper.__name__ = function.__name__
    return wrapper


@godzilla.route("/admin_dash")
@godzilla_required
def admin_dash():
    return render_template("godzilla/admin_dash.html")


@godzilla.route("/add_stage", methods=["GET", "POST"])
@godzilla_required
def add_stage():
    form = StageFillingForm()
    stages = Stage.query.all()
    if form.validate_on_submit():
        if form.picture.data:
            fname = form.question.data[0:10] + str(form.stage.data)
            pic = add_challenge_pic(form.picture.data, fname)
        else:
            pic = "nothing.png"
        stage = Stage(
            stage=form.stage.data,
            question=form.question.data,
            ans=form.ans.data,
            picture=pic,
        )

        db.session.add(stage)
        db.session.commit()
        return redirect(url_for("godzilla.add_stage", form=form, stages=stages))

    return render_template("godzilla/add_stage.html", form=form, stages=stages)


@godzilla.route("/review", methods=["GET", "POST"])
@godzilla_required
def review():
    form = ReviewForm()
    submissions = Submission.query.filter_by(correct=1).all()
    users = User.query.all()
    now = datetime.now()
    if form.validate_on_submit():
        submission = Submission.query.filter_by(id=form.submission_id.data).first()
        user = User.query.filter_by(id=submission.by).first()
        if form.review.data == "Accept":
            submission.correct = 2
            if user.level == submission.stage:
                message = (
                    "Your Submission for the "
                    + classify[user.level]
                    + " upgrade on "
                    + now.strftime("%d %b %Y at %I:%M %p")
                    + " has been rejected because one of your previous submissions for this upgrade have been accepted."
                )
            else:
                message = (
                    "Congratulations! Your Submission for the "
                    + classify[user.level + 1]
                    + " upgrade on "
                    + now.strftime("%d %b %Y at %I:%M %p")
                    + " has been accepted. You are now promoted to "
                    + classify[user.level + 1]
                )
                user.level = submission.stage
                user.upgrade_time = submission.time
                stat = Stats(uid=user.id, level=user.level, uptime=submission.time)
                db.session.add(stat)
        else:
            submission.correct = 0
            message = (
                "Oops! Your Submission for the "
                + classify[user.level + 1]
                + " upgrade on "
                + now.strftime("%d %b %Y at %I:%M %p")
                + " did not meet the requirements for the upgrade."
            )

        notification = Notification(uid=user.id, message=message)

        db.session.add(notification)

        db.session.commit()
        return redirect(url_for("godzilla.review"))
    return render_template(
        "godzilla/review.html", submissions=submissions, form=form, users=users
    )


@godzilla.route("/announce", methods=["GET", "POST"])
@godzilla_required
def announce():
    form = AnnounceForm()
    if form.validate_on_submit():
        announcement = Announcement(message=form.message.data)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for("godzilla.announce"))
    return render_template("godzilla/announce.html", form=form)


@godzilla.route("/all_users")
@godzilla_required
def all_users():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("godzilla/users.html", users=users)


@godzilla.route("/dnotif", methods=["GET", "POST"])
@godzilla_required
def dnotif():
    form = NotifForm()
    if form.validate_on_submit():
        notif = Notification(uid=form.uid.data, message=form.message.data)
        db.session.add(notif)
        db.session.commit()
        return redirect(url_for("godzilla.dnotif"))
    return render_template("godzilla/dnotif.html", form=form)


@godzilla.route("/all_subs")
@godzilla_required
def all_subs():
    submissions = Submission.query.order_by(Submission.time.desc()).all()
    users = User.query.all()
    return render_template(
        "godzilla/all_subs.html", submissions=submissions, users=users
    )


@godzilla.route("/all_feeds")
@godzilla_required
def all_feeds():
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
    users = User.query.all()
    return render_template("godzilla/all_feeds.html", feedbacks=feedbacks, users=users)
