from flask import Flask, render_template
from flask import Blueprint

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route('/home')
def homepage ():
    return render_template('home.jinja')