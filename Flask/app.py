import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import os

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def connection():
    if request.method == 'POST':
            identifiant = request.values.get('identifiant')
            secret = request.values.get('secret')
            app.config['identifiant'] = identifiant
            app.config['secret']=secret

            if not identifiant:
                flash('Aucun identifiant rentré')
                return redirect(url_for(''))
            elif not secret:
                flash("Aucun mot de passe rentré")
                return redirect(url_for('')) 
            else:
                return redirect(url_for('connecter'))
    return render_template('connection.html') 

@app.route('/connecter')
def connecter(): 
    return render_template('connecter.html')
