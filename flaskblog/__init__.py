from flask import Flask
from flaskblog.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # from flaskblog.errors.handlers import errors
    from flaskblog.wolfs.routes import wolfs
    from flaskblog.stripe.routes import main
  
    # app.register_blueprint(errors)
    app.register_blueprint(wolfs)
    app.register_blueprint(main)
  
    return app