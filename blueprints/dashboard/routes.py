from blueprints.dashboard import dashboard
from flask import render_template, redirect, request, jsonify, make_response, g
from utils import auth_user


@dashboard.route('/', methods=['post', 'get'], strict_slashes=False)
@auth_user
def dashboard():
    return render_template('dashboard/main.html', user=g.user)