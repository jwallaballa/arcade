"""
src/models.py

This module defines the core SQLAlchemy models used in the application,
including players, games, scores, and achievements. It also defines the
many-to-many association between players and achievements.
"""



from src.extensions import db

# Association table for many-to-many between players and achievements
player_achievement = db.Table(
    'player_achievement',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id')),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievements.id'))
)


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    player_game_scores = db.relationship('PlayerGameScore', back_populates='player', cascade='all, delete-orphan')
    achievements = db.relationship(
        'Achievement',
        secondary=player_achievement,
        back_populates='players'
    )

    def __repr__(self):
        return f'<Player(id={self.id}, username={self.username})>'


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String)

    player_game_scores = db.relationship('PlayerGameScore', back_populates='game', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Game(id={self.id}, name={self.name})>'


class PlayerGameScore(db.Model):
    __tablename__ = 'player_game_score'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    player = db.relationship('Player', back_populates='player_game_scores')
    game = db.relationship('Game', back_populates='player_game_scores')

    def __repr__(self):
        return f'<PlayerGameScore(id={self.id}, player_id={self.player_id}, game_id={self.game_id}, score={self.score})>'


class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String)

    players = db.relationship(
        'Player',
        secondary=player_achievement,
        back_populates='achievements'
    )

    def __repr__(self):
        return f'<Achievement(id={self.id}, name={self.name})>'
