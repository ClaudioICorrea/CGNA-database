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

@bp.route("/show_genes", methods=["GET","POST"])
def show_genes():
    ## mostrar algo en pantalla 
    ## recuperar la ultima consulta
    ## busqueda de la consulta en la base de datos  en el orden specie-> chromosoma -> genes
    ## segun lo encontrado mostrar de forma ordenada la información   
    
    #db, c = get_db()
    #c.execute(
    #    'SELECT t.id, t.created_at, t.description, u.username, t.completed'
    #    ' FROM todo t JOIN user u on t.created_by = u.id where'
    #    ' t.created_by = %s ORDER BY created_at desc', (g.user['id'],)
    #)
    #luke = c.fetchall()
    return render_template('todo/index.html', todos=luke)