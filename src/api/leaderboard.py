"""
leadboard.py

This module defines the leaderboard API routes for the application.
It exposes an endpoint that retrieves the highest scores across all games,
along with the corresponding player initials and game names.

"""

from flask import Blueprint, jsonify
from sqlalchemy import desc
from ..extensions import db
from ..models import Player, Game, PlayerGameScore

bp = Blueprint('leaderboard', __name__, url_prefix='/api/v1/data')

@bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():

    """
    API endpoint to get the top scores across all games,
    along with the player's initials and the game name.
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

        # Format results for JSON response
        results = [
            {
                "game_name": game_name,
                "initials": username[:3].upper() if username else 'N/A',
                "score": score
            }
            for score, game_name, username in high_scores
        ]

        return jsonify(results)

    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return jsonify({"error": "Could not retrieve leaderboard data"}), 500