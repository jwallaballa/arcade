"""
achievement.py stores the endpoints that allows data to be sent, retrieved, updated and deleted from
the achievement table in the Arcade database.
"""

from flask import Blueprint, jsonify, request, abort
from ..models import db, Achievement, Game

bp = Blueprint('achievements', __name__, url_prefix='/achievements')


@bp.route('', methods=['GET'])
def index():
    """
    Retrieves all achievements, with optional filtering by game.
    e.g., /achievements?game_id=1
    """
    game_id = request.args.get('game_id', type=int)

    if game_id:
        # Check if the game exists before filtering
        game = Game.query.get(game_id)
        if not game:
            return abort(404, description=f"Game with ID {game_id} not found.")
        achievements = Achievement.query.filter_by(game_id=game_id).all()
    else:
        achievements = Achievement.query.all()

    result = [ach.serialize() for ach in achievements]
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    """Creates a new achievement for a specific game."""
    required_fields = ['points', 'game_id']
    if not all(field in request.json for field in required_fields):
        return abort(400)  # Bad Request

    points = request.json['points']
    game_id = request.json['game_id']

    # Check if the referenced game exists
    game = Game.query.get(game_id)
    if not game:
        return abort(404, description="Game not found.")

    new_achievement = Achievement(points=points, game_id=game_id)

    db.session.add(new_achievement)
    db.session.commit()

    return jsonify(new_achievement.serialize()), 201


@bp.route('/<int:id>', methods=['GET'])
def show(id):
    """Retrieves a single achievement by its ID."""
    achievement = Achievement.query.get_or_404(id)
    return jsonify(achievement.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id):
    """Updates an achievement's points."""
    achievement = Achievement.query.get_or_404(id)

    if 'points' in request.json:
        achievement.points = request.json['points']

    db.session.commit()
    return jsonify(achievement.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """Deletes an achievement by its ID."""
    achievement = Achievement.query.get_or_404(id)
    db.session.delete(achievement)
    db.session.commit()
    return jsonify({'message': f'Achievement {id} deleted successfully'}), 200