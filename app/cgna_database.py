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
@bp.route('/click_gene/<where_is>/<id_genes>')
def click_gene(where_is,id_genes):
    db, c = get_db()
    id_querie = querie = id_genes
    
    print(where_is,id_genes)
    # Lógica de la función click_gene()
    return show_genes(where_is,id_querie,querie,c,db) ## show_genes(where_is,id_querie,querie,c,db)

@bp.route('/filter', methods =["POST"])
def filter():
    condicion=request.form.get('condicion')
    print(condicion)
    return '' #render_template("cgna_database/show_info/show_chromosome.html")''
@bp.route("/show_genes", methods=["GET"])
def show_genes(where_is,id_querie,querie,c,db,filter=[]):
    if where_is == "chromosomes":
        c.execute(
            'SELECT id_chromosome, gbig, number_genes, size, alias, id_specie FROM chromosomes WHERE id_chromosome = %s',
                (id_querie,)
        )  
        data_chromosome = c.fetchall()   
        c.execute(
            'SELECT specie FROM species WHERE id_specie = %s',
                (data_chromosome[0]['id_specie'],)
        )
        specie = c.fetchall()[0]['specie'] 
        c.execute(
            'SELECT id_genes, bio_type, gene_type,size FROM genes WHERE id_chromosome = %s',
                 (id_querie,)
        )
        data_genes = c.fetchall()  
        return render_template("cgna_database/show_info/show_chromosome.html",specie = specie,querie = querie, data_chromosome=data_chromosome, data_genes = data_genes, c=c, db=db)
    elif where_is == "genes":
        c.execute(
            'SELECT id_genes, id_chromosome, gene_type, start, end, score, strand, frame, size, name_gen, bio_type FROM genes WHERE id_genes = %s',
                (id_querie,)
        )
        data_genes = c.fetchall() 
        #print(data_genes[0]['id_chromosome'])
        c.execute(
            'SELECT id_specie FROM chromosomes WHERE id_chromosome = %s',
                (data_genes[0]['id_chromosome'],)
        )
        id_specie = c.fetchall()[0]['id_specie']
        c.execute(
            'SELECT specie FROM species WHERE id_specie = %s',
                (id_specie,)
        )
        specie = c.fetchall()[0]['specie']
        return render_template("cgna_database/show_info/show_gene.html", data_genes = data_genes, specie=specie,  querie=querie, c=c, db=db)
    else:
        return  redirect(url_for("cgna_database.index"))
    return redirect(url_for("cgna_database.index"))
@bp.route("/donwload_genes", methods=["POST","GET"])
def donwload_genes():
    id_genes = request.form.getlist("id_genes")
    print(id_genes)
    return render_template("cgna_database/index.html")

@bp.route("/search", methods=["GET", "POST"])
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
            ######################Guardamos la consulta en la BD####################
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
            #################busquemos queries en la base de dato####################### 
            if querie is None:
                # no hay ninguna especificación de lo que se quiere
                querie =""
                c.execute(
                   'SELECT id_chromosome, gbig, number_genes, size, alias FROM chromosomes WHERE id_specie = %s',
                (id_specie,) 
                )
                data = c.fetchall()
                return render_template("cgna_database/show_info/show_specie.html", querie = querie, specie=specie, data=data)
            else:
                id_querie, where_is =search_database(id_specie,querie,c,db)
                print(where_is)
                return show_genes(id_querie, where_is,querie,c,db)
        return redirect(url_for("cgna_database.index"))
    return redirect(url_for("cgna_database.index"))

