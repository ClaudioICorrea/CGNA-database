from flask import ( Blueprint, render_template, request, redirect, url_for, current_app, g, flash,
)

bp = Blueprint("cgna_database", __name__, url_prefix="/")

from werkzeug.exceptions import abort
from app.db import get_db


@bp.route("/", methods=["GET"])
def index():
    return render_template("cgna_database/index.html")


@bp.route("/_login", methods=["GET"])
def _login():
    return render_template("cgna_database/auth/_login.html")


@bp.route("/", methods=["GET", "POST"])
def search_genes():
    if request.method == "POST":
        name_genes = request.form.get("name_genes")
        specie = request.form.get("specie")
        chromosome = request.form.get("chromosomes")
        print(name_genes)
        error = None
        if not specie and not chromosome and not name_genes:
            error = "invalid query..."
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            id_specie = int(specie) if specie else None
            id_chromosome = int(chromosome) if chromosome else None
            if g.user:
                c.execute(
                    "insert into queries (id_specie, id_chromosome, name_gen, created_by)"
                    " values (%s,%s,%s,%s)",
                    (id_specie, id_chromosome, name_genes, g.user["id"]),
                )
            else:
                c.execute(
                    "insert into queries (id_specie, id_chromosome, name_gen, created_by)"
                    " values (%s,%s,%s,%s)",
                    (id_specie, id_chromosome, name_genes, 1),
                )
            db.commit()
            return render_template("cgna_database/show_genes.html")
    return redirect(url_for("cgna_database.index"))
