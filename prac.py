from authlib.integrations.flask_client import OAuth
from flask import Flask,url_for,session,redirect
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
oauth = OAuth(app)

app.secret_key='Abdul'


google= oauth.register(
    name='google',
    client_id='573036828100-4e74ieru5vcqi361mul8c2p4odgdc22m.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid profile email'},
)



@app.route('/')
def hello_world():
    email=dict(session).get('email',None)
    return f"hello ,{email}!"

@app.route('/login')
def login():
    google=oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email']=user_info['email']
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)

#
