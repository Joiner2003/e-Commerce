from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key="inventarioMazda"

#config Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventario_mazda'
mysqldb = MySQL(app)

semilla = bcrypt.gensalt()

@app.route('/')
def main():
    if 'nombre' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')


@app.route('/signin', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'nombre' in session:
            cur = mysqldb.connection.cursor()
            sql = "SELECT u.codigo, u.nombre, u.apellidos, u.email, u.rol FROM usuarios u"
            cur.execute(sql)
            data = cur.fetchall()
            return render_template('signin.html', datas = data)
    else:
        return "render_template('signin.html')"
        

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        if 'nombre' in session:
            return render_template('index.html')
        else:
            return render_template('login.html')
    else:
        nombre1 = request.form['name1']
        nombre2 = request.form['name2']
        name = nombre1 + ' ' + nombre2
        apellido1 = request.form['lastName1']
        apellido2 = request.form['lastName2']
        lastname = apellido1 + ' ' + apellido2
        email = request.form['email']
        rol = 'FinalUser'
        password = request.form['passs']
        password_encode = password.encode("utf-8")
        password_encrypted = bcrypt.hashpw(password_encode, semilla)

        cur = mysqldb.connection.cursor()
         
        sql = "SELECT COUNT(1) FROM usuarios WHERE email = %s"
        cur.execute(sql,[email])
        usuario = cur.fetchone()
        print(usuario[0])
        if usuario[0] == 0:
            cur.execute('INSERT INTO usuarios (nombre, apellidos, email, rol, contraseña, created) VALUES (%s, %s, %s, %s, %s, %s)', (name.upper(), lastname.upper(), email.upper(), rol.upper(), password_encrypted, 'NOW()'))
            mysqldb.connection.commit()
        else:
            flash("Usuario ya existe")
            return render_template('signin.html')

        if 'nombre' in session:
            flash('Usuario Agregado')
            return render_template('signin.html')
        else:
            session['nombre'] = name.upper()
            session['apellidos'] = lastname.upper()
            session['email'] = email.upper()
            session['rol'] = rol.upper()

            flash('Usuario Agregado satisfactoriamente')
            return render_template('productos.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
            if 'nombre' in session:
                return render_template('login.html')
            else:
                return render_template('login.html')
    else:
        #Obtener datos de ususario de base de datos
        usuario = request.form['email']
        contraseña = request.form['contraseña']
        password_encrypted = contraseña.encode('utf8')
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cur.execute(sql,[usuario])

        usuario = cur.fetchone()
        cur.close()
        if usuario != None:
            password_encrypted_encode = usuario[5].encode()
            if bcrypt.checkpw(password_encrypted, password_encrypted_encode):
                session['nombre'] = usuario[1]
                session['apellidos'] = usuario[2]
                session['email'] = usuario[3]
                session['rol'] = usuario[4]
                return  redirect(url_for('dashboard'))
                
            else:
                flash("Congtraseña incorrecta", "alert-warning")
                return render_template('login.html')
        else:
            flash("El usuario no existe")
            print("El usuario no existe")
            return redirect(url_for('login'))
            

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'nombre' in session:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')

@app.route('/verusuarios' , methods=['GET'])
def verusuarios():
    if request.method == 'GET':
        if 'nombre' in session:
            cur = mysqldb.connection.cursor()
            sql = "SELECT u.codigo, u.nombre, u.apellidos, u.email, u.rol FROM usuarios u"
            cur.execute(sql)
            data = cur.fetchall()
            return render_template('verusuarios.html', datas = data)
    else:
        return "render_template('verusuarios.html')"


@app.route('/edituser', methods=['GET','POST'])
def edituser():
    if request.method == 'GET':
        if 'nombre' in session:
            return render_template('edituser.html')
        else:
            return render_template('login.html')
    else:
        emailSearcher = request.form['search_email']
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cur.execute(sql,[emailSearcher])
        usuario = cur.fetchone()
        cur.close()
        if usuario != None:
            nombres = usuario[1].split(' ')
            apellidos = usuario[2].split(' ')
            nombre1 = nombres[0]
            nombre2 = nombres[1]
            apellido1 = apellidos[0]
            apellido2 = apellidos[1]
            data = [nombre1, nombre2, apellido1, apellido2, usuario[3], usuario[5]]
            return render_template('edituser.html', datas = data)
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('edituser'))

@app.route('/updateuser', methods=['POST'])
def updateuser():
    nombre1 = request.form['name1']
    nombre2 = request.form['name2']
    name = nombre1 + ' ' + nombre2
    apellido1 = request.form['lastName1']
    apellido2 = request.form['lastName2']
    lastname = apellido1 + ' ' + apellido2
    email = request.form['email']
    password = request.form['passs']
    password_encode = password.encode("utf-8")
    password_encrypted = bcrypt.hashpw(password_encode, semilla)
    cur = mysqldb.connection.cursor()
    if password == "":
        cur.execute('UPDATE usuarios SET nombre = %s, apellidos = %s ,email = %s WHERE email = %s', (name, lastname, email, email))
        mysqldb.connection.commit()
        flash('Usuario actualizado')
        return redirect(url_for('edituser'))
    else:
        cur.execute('UPDATE usuarios SET nombre = %s, apellidos = %s ,email = %s , contraseña = %s WHERE email = %s', (name, lastname, email, password_encrypted, email))
        mysqldb.connection.commit()
        if session['email'] == email:
            logout()
        flash('Usuario actualizado')
        return redirect(url_for('edituser'))
    
@app.route('/deleteuser', methods=['GET','POST'])
def eliminarusuario():
    if request.method == 'GET':
        if 'nombre' in session:
            return render_template('deleteuser.html')
        else:
            return render_template('login.html')
    else:
        emailSearcher = request.form['search_email']
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cur.execute(sql,[emailSearcher])
        usuario = cur.fetchone()
        cur.close()
        if usuario != None:
            nombres = usuario[1].split(' ')
            apellidos = usuario[2].split(' ')
            nombre1 = nombres[0]
            nombre2 = nombres[1]
            apellido1 = apellidos[0]
            apellido2 = apellidos[1]
            data = [nombre1, nombre2, apellido1, apellido2, usuario[3], usuario[5]]
            return render_template('deleteuser.html', datas = data)
        else:
            flash('Usuario no encontrado')
            return render_template('deleteuser.html')

@app.route('/deluser', methods=['POST'])
def deluser():
    email = request.form['email']
    correo = email.lower()
    print("correo"+ correo)
    sql = "DELETE FROM usuarios WHERE email = ?;"
    cur = mysqldb.connection.cursor()
    #cur.execute(sql, (email, ))
    #cur.execute("DELETE FROM usuarios WHERE email = {email}".format(correo))
    cur.execute("""DELETE FROM usuarios  WHERE  email=%s""",(email))
    mysqldb.connection.commit()
    #cur.close()
    flash("Usuario Eliminado")
    print(email)
    return render_template('deleteuser.html')


@app.route('/admin', methods=['GET'])
def admin():
    #Si ya inicio session y tipo de usuario es admin o superAdmin -> dashboard administrativo
    #sino si inicio session y tipo de usuario es usuario final -> dashboard
    #sino index
    if usuario != '':
        if rol == 'finalUser':
            return "render_template('dashboard')"
        else:
            return "render_template('admin.html')"
    else:
        return index()


@app.route('/editarrol', methods=['GET','POST'])
def edititarrol():
    if usuario != '':
        if rol == 'superAdmin':
            return "render_template('editarrol.html')"
        else:
            return index()
    else:
        return index()

@app.route('/addproduct', methods=['GET','POST'])
def addProducto():
    if request.method == 'GET':
        if 'nombre' in session:
            cur = mysqldb.connection.cursor()
            sql = "SELECT p.codigo, p.nombre, p.descripcion, p.cant_disp_bodega, p.cant_min_requerida, p.proveedor FROM productos p"
            cur.execute(sql)
            data = cur.fetchall()
            return render_template('addproduct.html', datas = data)
        else:
            return render_template('login.html')
    else:
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantDisp = request.form['cantDispBod']
        cantMinReq = request.form['cantMinReq']
        proveedor = request.form['proveedor']

        cur = mysqldb.connection.cursor()
        sql = "SELECT COUNT(1) FROM productos WHERE codigo = %s"
        cur.execute(sql,[codigo])
        producto = cur.fetchone()
        if producto[0] == 0:
            cur.execute('INSERT INTO productos (codigo, nombre, descripcion, cant_disp_bodega, cant_min_requerida, proveedor) VALUES (%s, %s, %s, %s, %s, %s)', (codigo ,nombre.upper(), descripcion.upper(), cantDisp.upper(), cantMinReq.upper(), proveedor.upper()))
            mysqldb.connection.commit()
            cur.close()
            flash("producto agregado")    
            return render_template('addproduct.html')
        else:
            flash("producto ya existe")
            return render_template('addproduct.html')
    
@app.route('/editProduct', methods=['GET','POST'])
def editProduct():
    if request.method == 'GET':
        if 'nombre' in session:
            return render_template('editProduct.html')
        else:
            return render_template('login.html')
    else:
        codigoSearcher = request.form['search_codigo']
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM productos WHERE codigo = %s"
        cur.execute(sql,[codigoSearcher])
        producto = cur.fetchone()
        cur.close()
        if producto != None:
            return render_template('editProduct.html', datas = producto)
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('editProduct'))

@app.route('/updateproduct', methods=['POST'])
def updateproduct():
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    cantDisp = request.form['cantDispBod']
    cantMinReq = request.form['cantMinReq']
    proveedor = request.form['proveedor']
    cur = mysqldb.connection.cursor()
    
    cur.execute('UPDATE productos SET nombre = %s, descripcion = %s ,cant_disp_bodega = %s, cant_min_requerida = %s, proveedor = %s WHERE codigo = %s', (nombre, descripcion, cantDisp, cantMinReq, proveedor, codigo))
    mysqldb.connection.commit()
    flash('Producto actualizado')
    return redirect(url_for('editProduct'))
    

@app.route('/buscarproducto', methods=['GET','POST'])
def buscarproducto():
    if request.method == 'GET':
        if 'nombre' in session:
            return render_template('buscarproducto.html')
        else:
            return render_template('login.html')
    else:
        codigoSearcher = request.form['search_codigo']
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM productos WHERE codigo = %s"
        cur.execute(sql,[codigoSearcher])
        producto = cur.fetchone()
        cur.close()
        if producto != None:
            return render_template('buscarproducto.html', datas = producto)
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('buscarproducto'))

@app.route('/eliminarProducto', methods=['GET','POST'])
def eliminarProducto():
    if usuario != '':
        if rol == 'finalUser':
            flash('No tiene permisos de eliminar productos')
            return "render_template('dashboard')"
        else:
            return "render_template('eliminarproducto.html')"
    else:
        return index()


@app.route('/buscarproducto', methods=['GET','POST'])
def buscar_producto():
    if usuario != '':
        return "render_template('buscarproducto.html')"
    else:
        return index()

@app.route('/listarproductos', methods=['GET'])
def listar_productos():
    if usuario != '':
        return render_template('inventory.html', data = usuario)
    else:
        return index()

@app.route('/productosdisponibles')
def productDisponibles():
    usuario = 'as'
    if usuario != '':
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM productos WHERE cant_disp_bodega > 0"
        cur.execute(sql)
        data = cur.fetchall()
        return render_template('productos.html', datas = data )
    else:
        return index()

if __name__ == '__main__':
    app.run(port=3000, debug=True)