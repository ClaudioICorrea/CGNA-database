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

def search_database(id_specie,querie,c,db):
    where_is=None
    id_querie=None
    
    # buscamos primeramente en la tabla de chromosomas 
    c.execute(
        'SELECT id_chromosome, alias FROM chromosomes WHERE id_specie = %s',
    (id_specie,)
    )
    data = c.fetchall()
    for dato in data:
        ### buscamos si existen coincidencias con id_chromosomes
        if dato['id_chromosome'] == querie:
            where_is = 'chromosomes'
            id_querie = dato['id_chromosome']
            return where_is, id_querie
        ### buscamos si existen coincidencias con los alias que tiene el chromosoma 
        alias=dato['alias'].split(",")
        for element in alias:
            if querie == element:
                where_is = 'chromosomes'
                id_querie = dato['id_chromosome']
                return where_is, id_querie
        # buscamos primeramente en la tabla de chromosomas 
    c.execute(
    'SELECT id_genes, name_gen FROM genes'
    )
    data = c.fetchall()
    for dato in data:
        if dato['id_genes'] == querie:
            where_is = 'genes'
            id_querie = dato['id_genes']
            return where_is, id_querie
    return where_is, id_querie
def show_genes():
    return redirect(url_for("cgna_database.index"))

@bp.route("/", methods=["GET", "POST"])
def search_genes():
    if request.method == "POST":
        querie = request.form.get("querie")
        id_specie = request.form.get("specie")
        data=[]
        error = None
        if not id_specie and not querie:
            error = "invalid query..."
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            id_specie = int(id_specie) if id_specie else None
            querie = str(querie) if querie else None
            ######################Guardamos la consulta en BD####################
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
            #############Buscamos la informacion de planta##############################
            c.execute(
                    'SELECT * FROM species WHERE id_specie = %s',
                (id_specie,) 
                )
            specie = c.fetchall()
            db.commit()
            #################busquemos queries en la base de dato####################### 
            if querie is None:
                # no hay ninguna especificación de lo que se quiere
                querie =""
                c.execute(
                   'SELECT id_chromosome, gbig, number_genes, size, alias FROM chromosomes WHERE id_specie = %s',
                (id_specie,) 
                )
                data = c.fetchall()
            else:
                id_querie, where_is =search_database(id_specie,querie,c,db)
                print('estoy aqui !!',id_querie,where_is)
                
                    
                    #if dato['id_chromosome'] == querie:
                     #   where_is = 'chromosomes'
                     #   id_querie = dato['id_chromosome']

            
            return render_template("cgna_database/show_info/show_specie.html", querie = querie, specie=specie, data=data)
    return redirect(url_for("cgna_database.index"))



    
    
    
    
    
    
    
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