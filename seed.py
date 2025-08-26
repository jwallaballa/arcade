"""
Seed.py is used to script fake data to the Postgres database.

Make sure to run this before checking out the leaderboard section of the app.

"""

import random
from faker import Faker
from src.app import create_app
from src.extensions import db
from src.models import Player, Game, PlayerGameScore, Achievement

fake = Faker()

def seed_database():
    """Seeds the database with random data each run."""
    app = create_app()
    with app.app_context():
        try:
            # Drop all existing tables and recreate them
            db.drop_all()
            db.create_all()
            print("Tables dropped & recreated.")

            # ---- Seed Games ----
            games = []
            for _ in range(5):  # create 5 random games
                game = Game(
                    name=fake.word().title(),
                    description=fake.sentence(nb_words=8)
                )
                games.append(game)
            db.session.add_all(games)

            # ---- Seed Players ----
            players = []
            for _ in range(5):  # create 5 random players
                player = Player(username=fake.first_name())
                players.append(player)
            db.session.add_all(players)
            db.session.commit()
            print("Random Games and Players seeded.")

            # ---- Seed Scores ----
            player_game_scores = []
            for player in players:
                for game in games:
                    if random.random() < 0.6:
                        score = PlayerGameScore(
                            player_id=player.id,
                            game_id=game.id,
                            score=random.randint(100, 5000)
                        )
                        player_game_scores.append(score)
            db.session.add_all(player_game_scores)

            # ---- Seed Achievements ----
            achievements = []
            for _ in range(3):
                achievement = Achievement(
                    name=fake.catch_phrase(),
                    description=fake.sentence(nb_words=10)
                )
                achievements.append(achievement)
            db.session.add_all(achievements)

            db.session.commit()
            print("Random Scores and Achievements seeded.")

        except Exception as e:
            db.session.rollback()
            print(f" An error occurred during seeding: {e}")
        finally:
            db.session.close()

if __name__ == '__main__':
    seed_database()
