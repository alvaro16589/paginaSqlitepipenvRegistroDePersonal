from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseDeDatos/tasks.db'
db = SQLAlchemy(app)#crea un cursor a la base de datos

@app.route('/')
def principal():
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug= True)#para que el servidor se inicie cada vez que exista un cambio en el archivo app.py ///codigo inicial