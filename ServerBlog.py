from flask import Flask, escape, session, request, Response, redirect, url_for, render_template, Markup
import pymysql

'''
Importante! hay que arrancar el servidor MySQL 
En windows:
ruta_del_Mysql\bin
mysqld --console

En Linux: seguramente lo tengáis levantado como servicio
systemctl status mysqld 
service mysqld status
'''

#Se necesita un servidor MySQL, con lo siguiente:
'''
create database usuarios
create table usuarios (email varchar(64), clave varchar(32), created timestamp default CURRENT_TIMESTAMP, primary key (email));
insert into usuarios (email, clave) values ('caca@oloro.sa','123abc');
insert into usuarios (email, clave) values ('vegeta@gmail.com','777');
'''

#Para probar el SQLInjection
'''
vegeta@gmail.com
' or 1=1  -- '
'''

#Para probar el XSS
'''
<script type="text/javascript">
var temp = document.getElementById("loginFrame");
delete temp.src;
temp.srcdoc='<!DOCTYPE html><html lang="en"><head>    <meta charset="UTF-8">    <title>Cutre Login</title></head><body><form action="http://127.0.0.1:5005/validateLogin" id="formLogin" method="POST">  <label for="user">user:</label>  <input type="text" id="user" name="user"><br><br>  <label for="pass">pass:</label>  <input type="password" id="pass" name="pass"><br><br>  <input type="submit" value="Submit"></form></body></html>';
</script>
'''

#Evidentemente, esto NUNCA se hace así, y a fuego
db = pymysql.connect("127.0.0.1","root","root","seguridad")
cursor = db.cursor()

app = Flask(__name__, template_folder='templates')

#Evidentemente esto JAMÁS debería estar subido al repositorio, recordad que esto es un taller!
app.secret_key = b'_5#y2L"Fadsf\t4Q8zx\n\xec]/'

#Esto debería estar en base de datos, pero para ahorrarme tener que preparar la base de datos, pues tiro por aquí
comentarios = [('ZanahoriaLetal','Qué bobada! no me interesa'), ('FanDelSalmón','¿pero qué narices?')]

@app.route("/blobPage")
def blobPage():
    respuesta = render_template("BlogPage.html", comentarios=comentarios)
    return respuesta

@app.route("/")
def defaultHome():
    return redirect(url_for('blobPage'))

@app.route("/validateLogin", methods=['GET', 'POST'])
def validarLogin():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']
        print("user: " + user)
        print("pass: " + password)
        query = "select count(1) from usuarios where email='"+user+"' and clave = '"+password+"'"
        print(query)
        cursor.execute(query)
        results =cursor.fetchall()
        for row in results:
            total = row[0]
            break
        if total > 0:
            session['logged'] = user
    return showLogin()

@app.route("/login.html")
def showLogin():
    if 'logged' in session:
        respuesta = render_template("logged.html", user=session['logged'])
    else:
        respuesta = render_template("login.html")
    return respuesta

@app.route("/logout", methods=['GET', 'POST'])
def logOut():
    session.pop('logged', None)
    return showLogin()

@app.route("/addComment", methods=['POST'])
def addComment():
    if 'logged' in session:
        #A ver, flask por defecto escapa los caracteres peligrosos. He tenido que recurrir al Markup para poder mostrar en qué consiste el XSS.
        comentarios.append((session['logged'],Markup(request.form['comment'])))
        respuesta = blobPage()
    else:
        respuesta = render_template("error.html")
    return respuesta


@app.route("/favicon.ico")
def favIcon():
    return ""

@app.route("/<page>")
def genericPage(page):
    respuesta = render_template(page)
    return respuesta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')

