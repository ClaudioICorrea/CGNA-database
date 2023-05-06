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
        querie = request.form.get("querie")
        specie = request.form.get("specie")
        data=[]
        error = None
        if not specie and not querie:
            error = "invalid query..."
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            id_specie = int(specie) if specie else None
            querie = str(querie) if querie else None
            if g.user:
                c.execute(
                    "INSERT INTO queries (id_specie, created_by,querie)"
                    " VALUES (%s,%s,%s)",
                    (id_specie, g.user["id"],querie),
                )
            else:
                c.execute(
                    "INSERT INTO queries (id_specie, created_by , querie)"
                    " VALUES (%s,%s,%s)",
                    (id_specie,1,querie),
                )
            db.commit()
            if querie is None:
                querie =""
                c.execute(
                    'SELECT id_chromosome, gbig, number_genes, size, alias FROM chromosomes WHERE id_specie = %s',
                (specie,) 
                )
                data = c.fetchall()
                c.execute(
                    'SELECT * FROM species WHERE id_specie = %s',
                (specie,) 
                )
                specie = c.fetchall()
                print(data)
                print(specie)
            
            return render_template("cgna_database/show_genes.html", querie = querie, specie=specie, data=data)
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