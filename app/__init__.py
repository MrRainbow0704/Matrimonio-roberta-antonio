from flask import Flask
import config
from . import tools


app = Flask(__name__, root_path=config.ROOT_DIR)
app.secret_key = config.SECRET_KEY
app.config["UPLOAD_FOLDER"] = config.UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = config.MAX_UPLOAD_SIZE

app.jinja_env.globals["is_logged_in"] = tools.is_logged_in
app.jinja_env.globals["generate_csrf_token"] = tools.generate_csrf_token

from . import routes
