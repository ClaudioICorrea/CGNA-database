import functools

from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    request,
    url_for,
    session,
    redirect,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        db, c = get_db()
        c.execute("SELECT id FROM user WHERE username = %s", (username,))
        if not username:
            error = "Nombre usuario es requerido"
        if not password:
            error = "Password es requerido"
        elif c.fetchone() is not None:
            error = "Usuario {} se encuentra registrado.".format(username)
        if error is None:
            c.execute(
                "INSERT INTO user (username, password) values (%s, %s)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for("cgna_database._login"))
    return render_template("cgna_database/auth/register.html", error=error)


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        error = None
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        c.execute("SELECT * FROM user where username = %s", (username,))
        user = c.fetchone()
        if user is None:
            error = "Usuario inválido"
        elif not check_password_hash(user["password"], password):
            error = "contraseña inválida"
        if error is None:
            print("estube aqui !!!")
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("cgna_database.index"))
    return render_template("cgna_database/auth/_login.html", error=error)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
