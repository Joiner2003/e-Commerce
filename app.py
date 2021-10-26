from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
#import bcrypt


app = Flask(__name__)
app.secret_key="BurberryGroup"

#configuracion BaseDatos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bgdatabase'
mysqldb = MySQL(app)

#semilla = bcrypt.gensalt()

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
                return render_template('login.html')
    else:
        #Obtener datos de ususario de base de datos
        Usuario = request.form['usuario']
        contraseña = request.form['contraseña']
       # password_encrypted = contraseña.encode('utf8')
        cur = mysqldb.connection.cursor()
        sql = "SELECT * FROM logins WHERE Usuario = %s"
        cur.execute(sql,[Usuario])


        Usuario = cur.fetchone()
        cur.close()
        if Usuario != None:
            #password_encrypted_encode = Usuario[5].encode()
            #if bcrypt.checkpw(password_encrypted, password_encrypted_encode):
            return  redirect(url_for('dashboard'))
               
                #session['nombre'] = usuario[1]
                #session['apellidos'] = usuario[2]
                #session['email'] = usuario[3]
                #session['rol'] = usuario[4]
                #return render_template('productos.html')"""
                
                
                

            #else:
             #   flash("Congtraseña incorrecta", "alert-warning")
              #  return render_template('login.html')
        else:
            flash("El usuario no existe")
            print("El usuario no existe")
            return redirect(url_for('login'))
    

@app.route('/Registro', methods=['GET','POST'])
def Registro():
    return render_template('Register.html')

@app.route('/principal', methods=['GET', 'POST'])
def principal():
    return render_template('PaginaPrincipal.html')

@app.route('/dashboard')
def dashboard():
    if 'Usuario' in session:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')

@app.route('/ListaDeseos', methods=['GET', 'POST'])
def ListaDeseos():
    return render_template('ListaDeDeseos.html')

@app.route('/EliminarProductos',methods=['GET', 'POST'])
def EliminarProductos():
    return render_template('eliminarProducto.html')

@app.route('/Comentarios', methods=['GET', 'POST'])
def Comentarios():
    return render_template('Comentarios.html')