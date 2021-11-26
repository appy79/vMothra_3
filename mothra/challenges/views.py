from os import environ
from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from mothra import db, start, end
from mothra.models import (
    User,
    Submission,
    Attempts,
    Stage,
    Notification,
    Announcement,
    Stats,
)
from mothra.forms import SubmissionForm
from mothra.views import classify
from datetime import datetime
import os


challenges = Blueprint("challenges", __name__)

# SUBMISSION HANDLING


def sub(form, attemp):
    now = datetime.now()
    if now > end:
        flash("The submission time is over. No new answers will be accepted.")
        return redirect(url_for("index"))
    att = Attempts.query.filter_by(
        of=current_user.id, stage=current_user.level + 1
    ).first()
    if att:
        if att.atmpts >= attemp:
            flash("You have exhausted your number of attempts at this problem.")
            abort(403)
        else:
            att.atmpts += 1
    else:
        atmpt = Attempts()
        db.session.add(atmpt)
    ans = form.ans.data
    corans = Stage.query.filter_by(stage=current_user.level + 1).first()
    if ans != corans.ans:
        correct = 0
        message = (
            "Oops! Your Submission for the "
            + classify[current_user.level + 1]
            + " upgrade on "
            + now.strftime("%d %b %Y at %I:%M %p")
            + " has been auto rejected because your answer was incorrect."
        )
    else:
        correct = 1
        message = (
            "Your Submission for the "
            + classify[current_user.level + 1]
            + " upgrade on "
            + now.strftime("%d %b %Y at %I:%M %p")
            + " has been sent for review. Please wait for some time."
        )
    sub = form.sub.data
    submission = Submission(ans=ans, sub=sub, correct=correct)
    notification = Notification(uid=current_user.id, message=message)
    flash(message)
    db.session.add(submission)
    db.session.add(notification)
    db.session.commit()


# MESSAGING


@challenges.route("/notifications")
@login_required
def notifications():
    notifs = Notification.query.filter_by(uid=current_user.id).all()
    notifs.reverse()
    count = Notification.query.filter_by(uid=current_user.id).count()
    current_user.notif_count = count
    db.session.commit()
    return render_template("notifications.html", notifs=notifs)


# CHALLENGE ROUTES


@challenges.route("/challenge/<int:clevel>", methods=["GET", "POST"])
@login_required
def challenge(clevel):
    print(clevel)
    if datetime.now() < start and current_user.user_type != "Godzilla":
        flash("Event has not yet started.")
        return redirect(url_for("index"))

    if current_user.level >= clevel:
        stats = Stats.query.filter_by(level=clevel, uid=current_user.id).first()
        stage = Stage.query.filter_by(stage=clevel).first()
        return render_template(
            "challenge.html", stage=stage, stats=stats, clevel=clevel
        )

    elif current_user.level >= 7:
        return render_template("wip.html")
    else:
        form = SubmissionForm()
        att = int(os.environ.get("ATTEMPTS"))
        attempts = Attempts.query.filter_by(
            of=current_user.id, stage=current_user.level + 1
        ).first()
        stage = Stage.query.filter_by(stage=current_user.level + 1).first()
        if form.validate_on_submit():
            sub(form, att)
            return redirect(
                url_for("challenges.challenge", clevel=current_user.level + 1)
            )

        return render_template(
            "challenge.html", form=form, attempts=attempts, att=att, stage=stage
        )
