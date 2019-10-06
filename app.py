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
    idprop = db.Column(db.Integer)

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

@app.route('/borrarprop/<idprop>')
def borrarprop(idprop):
    propie = tbpropietario.query.filter_by(idpropietario=int(idprop)).first()
    masc = tbmascota.query.filter_by(idprop=int(idprop))
    db.session.delete(propie)
    for i in masc:
        db.session.delete(i)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/actu/<idprop>')
def actuaUsua(idprop):
    propie = tbpropietario.query.filter_by(idpropietario = int(idprop)).first()
    db.session.commit()
    return render_template('actualizaru.html',propietario = propie)

@app.route('/actualizarprop', methods = ['POST'])
def actualizarprop():
    propie = tbpropietario.query.filter_by(idpropietario = int(request.form['idu'])).first()
    propie.nombre = request.form['nomb']
    propie.apellido = request.form['ape']
    propie.telefono = int(request.form['telf'])
    propie.anio = int(request.form['anio'])
    propie.sexo  = request.form['sxo']
    db.session.commit()
    return redirect(url_for('principal'))

@app.route('/crearmasc/<idpropi>',methods = ['POST'])
def crearmascota(idpropi):
    masco = tbmascota(nombre = request.form['nombmas'],anio = request.form['aniomas'],sexo = request.form['sxomas'],idprop =int(idpropi) )
    db.session.add(masco)
    db.session.commit()
    return redirect(url_for('verMascotas',idprop=int(idpropi)))

@app.route('/borrarmasc/<idmasc> <idpropi>')    
def borrarmasco(idmasc,idpropi):
    masc = tbmascota.query.filter_by(idmascota=int(idmasc)).first()
    db.session.delete(masc)
    db.session.commit()
    return redirect(url_for('verMascotas',idprop=int(idpropi)))

@app.route('/mascota/<idprop>')#direccionando a la pagina para ver las mascotas
def verMascotas(idprop):
    propie = tbpropietario.query.filter_by(idpropietario=int(idprop)).first()
    revmascota = tbmascota.query.all()
    db.session.commit()
    return render_template('mascotas.html',propietario=propie,qrymascota=revmascota)

if __name__=='__main__':
    app.run(debug= True)#para que el servidor se inicie cada vez que exista un cambio en el archivo app.py ///codigo inicial