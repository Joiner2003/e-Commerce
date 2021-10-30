from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key="BurberryGroup"

#configuracion BaseDatos
app.config['MYSQL_HOST'] = 'e-commerceuninorte.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'Uninorte@e-commerceuninorte'
app.config['MYSQL_PASSWORD'] = 'Unorte2021'
app.config['MYSQL_DB'] = 'bgdatabase'
mysqldb = MySQL(app)

semilla = bcrypt.gensalt()

@app.route('/')
def main():
    if 'Usuario' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')
    
    
@app.route('/login', methods=['GET','POST'] )
def iniciarSesion():
    if request.method == 'GET':
        if 'Usuario' in session:
            return render_template('login.html')
        else:
            return render_template('Register.html')
    else:
        #Obtener datos de ususario de base de datos
        Usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        password_encrypted = contraseña.encode('utf8')
        
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM Registro WHERE Usuario = %s"
        cur.execute(sql,[Usuario])

        Usuario = cur.fetchone()
        cur.close()
        
        Rol = request.form['roles']
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM Registro WHERE Roles = %s"
        cur.execute(sql,[Rol])

        Rol = cur.fetchone()
        cur.close()
        if Usuario != None and rol == "Admin":
            #password_encrypted_encode = Usuario[5].encode()
            #if bcrypt.checkpw(password_encrypted, password_encrypted_encode):
            return  redirect(url_for('dashboard'))
        elif Usuario != None and rol == "cliente":
            return  redirect(url_for('principal'))
        else:
            flash("El usuario no existe")
            print("El usuario no existe")
            return redirect(url_for('Registro'))
    

@app.route('/Registro', methods=['GET','POST'])
def Registro():
    
    
    if request.method == 'GET':
        if 'Usuario' in session:
            return render_template('login.html')
        else:
            return render_template('Register.html')
    else:
        nombre = request.form['nombre']
        apellido = request.form['Apellido']
        Ide = request.form['Ide']
        email = request.form['Email']
      #  rol = 'FinalUser'
        usuario = request.form['Usuario']
        password = request.form['Contraseña']
        rol = request.form['roles']
        password_encode = password.encode("utf-8")
        password_encrypted = bcrypt.hashpw(password_encode, semilla)

        cur = mysqldb.connection.cursor()
        cur.execute('INSERT INTO registro (Nombre, Apellido, Id, Email, Usuario, Contraseña,Roles) VALUES (%s, %s, %s, %s, %s, %s, %s)', (nombre.upper(), apellido.upper(), Ide.upper(), email.upper(), usuario.upper(),password_encrypted,rol.upper()))
        mysqldb.connection.commit()


        flash('Usuario Agregado satisfactoriamente')
        return render_template('login.html')


@app.route('/principal', methods=['GET', 'POST'])
def principal():
    return render_template('PaginaPrincipal.html')

@app.route('/dashboard')
def dashboard():
    if 'Usuario' in session:
        return render_template('dashboard.html')
    else:
        return render_template('dashboard.html')

@app.route('/ListaDeseos', methods=['GET', 'POST'])
def ListaDeseos():
    return render_template('ListaDeDeseos.html')

@app.route('/EliminarProductos',methods=['GET', 'POST'])
def EliminarProductos():
    return render_template('eliminarProducto.html')

@app.route('/Comentarios', methods=['GET', 'POST'])
def Comentarios():
    return render_template('Comentarios.html')

if __name__ == '__main__':
    app.run(port=5500, debug=True)