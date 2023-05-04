import subprocess
import os


def run_flask():
    if os.path.exists("venv/Scripts/activate"):
        print("Inicializando...")
        print("start APP in Flask..")
        os.environ["FLASK_APP"] = "app"
        subprocess.call(["flask", "init-db"])

    else:
        print("virtualizado aplicacion...")
        subprocess.call(["python", "-m", "venv", "venv"])
        subprocess.call([".", "venv/Scripts/activate"])
        subprocess.call(["pip", "install", "Flask"])
        subprocess.call(["pip", "install", "werkzeug"])
        subprocess.call(["pip", "install", "mysql-connector-python"])
        subprocess.call(["pip","install","biopython"])
        #pip install cffconvert
        #pip install bcbio-gff
        subprocess.call(["pip", "install", "python-dotenv"])

        print("start APP in Flask..")
        os.environ["FLASK_APP"] = "app"
        print("start database")
        subprocess.call(["flask", "init-db"])

    # pip install werkzeug
    # pip install mysql-connector-python
    # python -m venv venv
    # . venv/Scripts/activate
    # pip install Flask

    print("start database")
    subprocess.call(["python", "_bio.py"])
    print("start APP as development..")
    os.environ["FLASK_DEBUG"] = "on"
    print("flask run..")
    subprocess.call(["flask", "run"])
    
    # subprocess.call(["set"])
    print("Done")


run_flask()
