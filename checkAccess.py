
from flask import session, redirect, url_for
from functools import wraps
#decorate function to prevent access if not log in -Sherman
def checkAccess(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if "username" in session and "id" in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap