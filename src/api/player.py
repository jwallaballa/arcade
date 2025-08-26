"""

player.py stores the endpoints that allows data to be sent, retrieved, updated and deleted from
the player table in the Arcade database
"""

from flask import Blueprint, jsonify, request, abort
from ..models import db, Player

bp = Blueprint('players', __name__, url_prefix='/players')


@bp.route('', methods=['GET'])
def index():
    players = Player.query.all()
    result = []
    for p in players:
        result.append(p.serialize())
    return jsonify(result)


@bp.route('', methods=['POST'])
def create():
    if 'initials' not in request.json:
        return abort(400)

    initials = request.json['initials']
    new_player = Player(initials=initials)
    db.session.add(new_player)
    db.session.commit()
    return jsonify(new_player.serialize()), 201


@bp.route('/<int:id>', methods=['GET'])
def show(id):
    player = Player.query.get_or_404(id)
    return jsonify(player.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id):
    player = Player.query.get_or_404(id)
    if 'initials' not in request.json:
        return abort(400)

    player.initials = request.json['initials']
    db.session.commit()
    return jsonify(player.serialize()), 200


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Player deleted'}), 200