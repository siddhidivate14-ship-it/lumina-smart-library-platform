from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import or_
from extensions import db
from models import Member

members_bp = Blueprint("members", __name__, url_prefix="/members")

@members_bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    query = Member.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Member.name.ilike(like), Member.member_code.ilike(like), Member.email.ilike(like)))
    members = query.order_by(Member.id.desc()).all()
    return render_template("members/index.html", members=members, q=q)

@members_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        code = request.form.get("member_code", "").strip().upper()
        if Member.query.filter_by(member_code=code).first():
            flash("Member code already exists.", "danger")
            return render_template("members/form.html")
        member = Member(
            member_code=code,
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            department=request.form.get("department", "").strip(),
        )
        db.session.add(member)
        db.session.commit()
        flash("Member registered successfully.", "success")
        return redirect(url_for("members.index"))
    return render_template("members/form.html")
