import os
from datetime import datetime
from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, flash
from flask_cors import CORS
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.google import make_google_blueprint, google
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from requests import get
from exceptions.request_exceptions import MalformedRequestException, MissingParameterException, EntityNotFoundException
from model.DynamoDBOAuthStorage import DynamoDBStorage, OAuth
from model.User import User
from routes.translationRoutes import translation_routes
from routes.userRoutes import user_routes

load_dotenv()
IS_DEV = environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER_HOST = "http://localhost:3000"
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

print(client_id, client_secret)
app = Flask(__name__)
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
# app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

toolbar = DebugToolbarExtension(app)
CORS(app)

google_blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)
google_blueprint.storage = DynamoDBStorage(OAuth, user=current_user)
app.register_blueprint(google_blueprint, url_prefix="/login")
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(translation_routes, url_prefix='/translation')
login_manager = LoginManager(app)

print("In app.py")
questionNumber = 0
questions = [{
    "id": 1,
    "sentence": "Ich gehe in die Berliner Kirche",
    "answer": 1,
    "choices": ["ins", "in die", "auf der", "zum"]
},
    {
        "id": 2,
        "sentence": "Ich bin stärker als meine Angst",
        "answer": 1,
        "choices": ["besser", "stärker", "schwacher", "großer"]
    }]


def proxy(host, path):
    response = get(f"{host}{path}")
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return response.content, response.status_code, headers


# @app.route("/")
# def hello_world():
#     return "<body><p>Hello test, World!</p></body>"

@login_manager.user_loader
def load_user(user_id: str) -> User:
    """Load the user with the given id."""
    print("In load user: " + user_id)
    return User.safe_get(user_id)


@app.route("/logout")
@login_required
def logout():
    print(f"Logging user {current_user} out".format(current_user=current_user))
    del google_blueprint.token
    logout_user()
    return redirect("/")


@oauth_authorized.connect
def google_log_in(blueprint, token):
    print(f"Signed in successfully with {blueprint.name}; {blueprint.__dict__}")
    print(f"Token: {token}")
    resp = google.get("/oauth2/v1/userinfo")
    response = resp.json()
    username = response["email"].split("@")[0]
    email = response["email"]
    profile_img_url = response["picture"]
    user = User.safe_get(username)
    if not user:
        user = User(username,
                    email=email,
                    preferred_language="eng",
                    languages_spoken={"eng"},
                    account_created=datetime.utcnow(),
                    profile_img_url=profile_img_url)
        user.save()
    login_user(user=user)

    print(user.__json__())
    print(dir(blueprint))
    return True
    # If existing account, redirect to home/last page
    # Otherwise, redirect to finish create User page


# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = "OAuth error from {name}! " "message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


@app.route("/question")
def get_question():
    return jsonify(questions)


@app.route("/currentUser")
def get_current_user():
    if current_user.is_authenticated:
        return str(current_user)
    else:
        return "No current user"


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def get_app(path):
    if not current_user.is_authenticated:
        return redirect("login/google")
    if google.authorized:
        resp = google.get("/oauth2/v1/userinfo")
        print("You are {email} on Google".format(email=resp.json()['email']))
    else:
        print("User not authorized")

    print("Current user {current_user}".format(current_user=current_user))
    print(type(current_user))
    if IS_DEV:
        return proxy(WEBPACK_DEV_SERVER_HOST, request.path)
    if 'assets' in path:
        return app.send_static_file('assets/' + path.split('/')[-1])
    return app.send_static_file(path)


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.errorhandler(MalformedRequestException)
def handle_malformed_request_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(MissingParameterException)
def handle_malformed_request_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(EntityNotFoundException)
def handle_malformed_request_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(Exception)
def all_exception_handler(error):
    if hasattr(error, "code"):
        return "Error: " + str(error.code)
    return str(error)
