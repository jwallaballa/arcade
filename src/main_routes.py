"""
main_routes.py

This module defines the primary web-facing routes for the arcade application.
It handles rendering of the homepage and leaderboard pages by integrating
with the database and templates.
"""

from flask import Blueprint, render_template
from sqlalchemy import desc
from .extensions import db
from .models import Player, Game, PlayerGameScore

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Render the main arcade homepage.
    """
    return render_template('arcade_app/index.html')

@bp.route('/leaderboard/')
def leaderboard():
    """
    Fetches leaderboard data from the database and renders the page.
    """
    try:
        high_scores = (
            db.session.query(
                PlayerGameScore.score,
                Game.name,
                Player.username
            )
            .join(PlayerGameScore, Game.id == PlayerGameScore.game_id)
            .join(Player, Player.id == PlayerGameScore.player_id)
            .order_by(desc(PlayerGameScore.score))
            .all()
        )

        results = [
            {
                "game_name": game_name,
                "initials": username[:3].upper() if username else 'N/A',
                "score": score
            }
            for score, game_name, username in high_scores
        ]

        return render_template('arcade_app/leaderboard.html', leaderboard_data=results)

    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return render_template('arcade_app/leaderboard.html', leaderboard_data=[], error="Failed to load leaderboard.")