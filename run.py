import subprocess
import os
#import getpass
import msvcrt





def run_flask():
    option=None
    if os.path.exists("venv/Scripts/activate"):
        print("Inicializando...")
        print("start APP in Flask..")
        os.environ["FLASK_APP"] = "app"
        while not option == 'Y' and not option == 'N':
            print('Is it required to initialize the database? N/Y')
            option = msvcrt.getch().decode('utf-8').upper()
        if option == 'Y':    
            print("initializing database..")
            subprocess.call(["flask", "init-db"])
            print("updating database..")
            subprocess.call(["python", "_bio.py"])
        

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

    
    print("start APP as development..")
    os.environ["FLASK_DEBUG"] = "on"
    print("flask run..")
    subprocess.call(["flask", "run"])
    
    # subprocess.call(["set"])
    print("Done")


run_flask()
