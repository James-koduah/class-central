from flask import session, abort, redirect, g
from mongodb_engine.users import users

def auth_user(function):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect('/login')  # Authorization required
        g.user = users.get_user(session.get('user'))
        return function()
    return wrapper
