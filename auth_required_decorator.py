from flask import Flask, request, Response
from functools import wraps

app = Flask(__name__)

def check_auth(username, password):
     return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/page')
@auth_required
def page():
    return 'you are on the page'

if __name__ == '__main__':
    app.run(debug=True)
