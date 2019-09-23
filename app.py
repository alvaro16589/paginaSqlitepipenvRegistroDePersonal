from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/Tienda.db'
db = SQLAlchemy(app)#crea un cursor a la base de datos

class tbpropietario(db.Model):
    idpropietario = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    telefono = db.Column(db.Integer)
    anio = db.Column(db.Integer)
    sexo = db.Column(db.String(5))

class tbmascota(db.Model):
    idmascota = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(20))
    anio = db.Column(db.Integer)
    sexo = db.Column(db.String(5))
    idpropietario = db.Column(db.Integer,foreign_key=tbpropietario.idpropietario)

@app.route('/')
def principal():
    revisarUs = tbpropietario.query.all()
    return render_template('index.html',qryPropietarios=revisarUs)

@app.route('/crearprop',methods=['POST'])
def crearpropietario():
    prop = tbpropietario(nombre = request.form['nomb'],apellido = request.form['ape'], telefono = request.form['telf'],anio = request.form['anio'], sexo = request.form['sxo'] )
    db.session.add(prop)#nos permite agregar contenido a la base de datos
    db.session.commit()#pone fin a la sesion de ingreso de datos
    return redirect(url_for('principal'))##redirecciona a una url que queramos en este caso home

@app.route('/mascota/<idprop>')#direccionando a la pagina para ver las mascotas
def verMacotas(idprop):
    propie = tbpropietario.query.filter_by(idpropietario=int(idprop)).first()
    db.session.commit()
    return render_template('mascotas.html',propietario=propie)

if __name__=='__main__':
    app.run(debug= True)#para que el servidor se inicie cada vez que exista un cambio en el archivo app.py ///codigo inicial