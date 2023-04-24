import subprocess
import os

def run_flask():
    if os.path.exists("venv/Scripts/activate"):
        print("Inicializando...")
    else:
        print("virtualizado aplicacion...")
        subprocess.call(["python","-m","venv","venv"])
        subprocess.call([".","venv/Scripts/activate"])
        subprocess.call(["pip","install","Flask"])
    # python -m venv venv
    # . venv/Scripts/activate
    # pip install Flask
    
    print('start APP in Flask..')
    os.environ['FLASK_APP'] = 'app'
    '''
    os.environ['FLASK_DATABASE_HOST'] = 'localhost'
    os.environ['FLASK_DATABASE_PASSWORD'] = 'lukemaster'
    os.environ['FLASK_DATABASE_USER'] = 'root'
    os.environ['FLASK_DATABASE'] = 'prueba'
    print('start database')
    subprocess.call(["flask","init-db"])
    
    
    '''
    
    print('start APP as development..')
    os.environ['FLASK_VPN'] = 'development'
    print('flask run..')
    subprocess.call(["flask","run"])
    
    #subprocess.call(["set"])
    print('Done')
    
run_flask()