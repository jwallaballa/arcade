
Jessica Wall || 08/26/2025

LuckyDucky Arcade -- Portfolio Project

LuckyDucky Arcade is a retro-themed web arcade built with Flask, SQLAlchemy, and PostgreSQL. 
It features multiple playable ASCII games, including Snake, Pong, and Tic-Tac-Toe, 
with session-based gameplay, interactive front-end using TailwindCSS, and a global leaderboard.
The project showcases full-stack development with RESTful APIs, database modeling, and front-end integration.


------------------------------------------------------------------------------------------------------------------------------------------------
FEATURES
- Play multiple games in the browser:
- Snake (AsciiSnakeGame)
- Pong (AsciiPongGame)
- Tic-Tac-Toe (TicTacToeGame)
- Neon-styled leaderboard displaying top scores.
- Session-based game state persistence.
- Responsive retro-themed UI with TailwindCSS.
- RESTful API endpoints to manage players, games, achievements, and scores.

------------------------------------------------------------------------------------------------------------------------------------------------
USAGE INSTRUCTIONS
- How to run locally:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask --app src.app run --debug
  (or flask run) 

- Leaderboard data
Please run seed.py to generate fake data for the /leaderboard section
cd .. 
python seed.py 

______________________________________________________________________________________________________
