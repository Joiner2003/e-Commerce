from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL


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
    if 'nombre' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')
    
    
@app.route('/login', methods=['GET','POST'] )
def iniciarSesion():
    if request.method == 'GET':
        if 'Usuario' in session:
            cur = mysqldb.connection.cursor()
            sql = "SELECT u.Idusuario, u.Usuario, u.Contraseña, FROM login u"
            cur.execute(sql)
            data = cur.fetchall()
            return render_template('login.html', datas = data)
    else:
        return "render_template('login.html')"
    

@app.route('/Registro', methods=['GET','POST'])
def Registro():
    return render_template('Register.html')

@app.route('/principal', methods=['GET', 'POST'])
def principal():
    return render_template('PaginaPrincipal.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
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