"""
game.py  stores the endpoints that allows data to be sent, retrieved, updated and deleted from
the game table in the Arcade database.
"""

from flask import Blueprint, jsonify, request, abort
from ..models import db, Game

bp = Blueprint('games', __name__, url_prefix='/games')


@bp.route('', methods=['GET'])
def index():
    """
    Retrieves all games, with optional sorting.
    e.g., /games?sort_by=high_score
    """
    sort_by = request.args.get('sort_by')
    if sort_by == 'high_score':
        games = Game.query.order_by(Game.high_score.desc()).all()
    else:
        games = Game.query.all()

    result = [game.serialize() for game in games]
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    """Creates a new game."""
    if 'title' not in request.json:
        return abort(400)  # Bad Request

    title = request.json['title']
    new_game = Game(title=title)

    db.session.add(new_game)
    db.session.commit()

    return jsonify(new_game.serialize()), 201


@bp.route('/<int:id>', methods=['GET'])
def show(id):
    """Retrieves a single game by its ID."""
    game = Game.query.get_or_404(id)
    return jsonify(game.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id):
    """Updates a game's title or high score."""
    game = Game.query.get_or_404(id)

    if 'title' in request.json:
        game.title = request.json['title']
    if 'high_score' in request.json:
        game.high_score = request.json['high_score']

    db.session.commit()
    return jsonify(game.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """Deletes a game by its ID."""
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': f'Game {id} deleted successfully'}), 200