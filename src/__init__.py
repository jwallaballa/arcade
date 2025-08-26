# src/__init__.py

import os
from flask import Flask
from .extensions import db, migrate
from dotenv import load_dotenv

# Import your existing blueprints
from .api.achievement import bp as achievement_bp
from .api.game import bp as game_bp
from .api.player import bp as player_bp
from .api.arcade_game import bp as arcade_game_bp
from .main_routes import bp as main_bp  # Import the main blueprint
from .api.leaderboard import bp as leaderboard_bp  # Import the leaderboard blueprint


def create_app(config_object="config.Config"):
    """
    Creates the Flask application instance.
    """
    # Load environment variables from a .env file for local development
    load_dotenv()

    app = Flask(__name__)

    # Configure the database from environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.environ['DATABASE_USER']}:"
        f"{os.environ.get('DATABASE_PASSWORD', '')}@"
        f"{os.environ['DATABASE_HOST']}:"
        f"{os.environ['DATABASE_PORT']}/"
        f"{os.environ['DATABASE_NAME']}"
    )

    # Configure the session
    app.secret_key = os.environ.get('SECRET_KEY', 'a-super-secret-key-that-should-be-in-env')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register API blueprints
    app.register_blueprint(achievement_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(arcade_game_bp)
    app.register_blueprint(main_bp)
    # app.register_blueprint(leaderboard_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
