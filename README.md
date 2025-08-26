
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


-------------------------------------------------------------------------------------------------------------------------------------------------

ENDPOINT	                        METHOD	            PARAMETERS	                                                        DESCRIPTION
/players	                        GET		                                                                                Retrieves a list of all players.
/players	                        POST	            {"initials": "string"}	                                            Creates a new player.
/players/<int:id>	                GET	                id: player ID	                                                    Retrieves a single player by ID.
/players/<int:id>	                PUT	                id: player ID, {"initials": "string"}	                            Updates a player's initials.
/players/<int:id>	                DELETE	            id: player ID	                                                    Deletes a player and all associated data.
/games	                            GET	                None	                                                            Retrieves a list of all games.
/games	                            POST	            {"title": "string", "high_score": "integer"}	                    Creates a new game.
/games/<int:id>	                    GET	                id: game ID	                                                        Retrieves a single game by ID.
/games/<int:id>	                    PUT	                id: game ID, {"title": "string"}	                                Updates a game's title.
/games/<int:id>	                    DELETE	            id: game ID	                                                        Deletes a game and all associated data.
/achievements	                    GET		                                                                              Retrieves a list of all achievements.
/achievements	                    POST	            {"points": "integer", "game_id": "integer"}	                        Creates a new achievement.
/achievements/<int:id>	            GET	                id: achievement ID	                                                Retrieves a single achievement.
/achievements/<int:id>	            PUT	                id: achievement ID, {"points": "integer"}	                        Updates an achievement's points.
/achievements/<int:id>	            DELETE	            id: achievement ID	                                                Deletes an achievement.
/players/<int:player_id>/scores	    POST	            player_id: player ID, {"game_id": "integer", "score": "integer"}	Adds a new score for a player in a specific game.
/arcade/play                        POST               {"game_name": "snake_ascii", "input": "start"}                      Handles game input and updates game state in session.
/api/v1/data/leaderboard            GET                 None                                                                Retrieves leaderboard data in JSON format.
-------------------------------------------------------------------------------------------------------------------------------------------------

--- How did the project's design evolve over time? ---
The project's design began with a simple relational database schema to manage players, games, achievements, and scores. Initially, I planned to use a single join table for both achievements and scores, but I soon realized a dedicated PlayerGameScore association model was necessary to accurately track scores and timestamps for each player-game relationship. This change required restructuring the API endpoints to better reflect the new data model.

As the project progressed, it evolved from a purely backend RESTful API to a full-stack arcade application. I implemented session-based game handling to support multiple simultaneous game instances, enabling players to interact with Snake, Pong, and Tic-Tac-Toe in real time. The frontend was enhanced with a retro, neon-styled interface using TailwindCSS, including interactive game boards, animated GIFs, and a responsive leaderboard that displays high scores dynamically.

Overall, the project now demonstrates both robust backend API design and immersive frontend game interaction, showcasing the full stack development process.

--- Did you choose to use an ORM or raw SQL? Why? ---
I chose to use an ORM, specifically SQLAlchemy. The main reason for this choice was to abstract away the direct SQL queries and manage the database schema using Python classes. This approach offered me  several advantages like:
-  Type Safety and Consistency: SQLAlchemy provides a more object-oriented way to interact with the database, reducing the chance of SQL injection vulnerabilities and making the code more readable and maintainable.
- Rapid Development: By defining relationships and models in Python, I could quickly build out the API endpoints without writing boilerplate SQL for every CRUD operation.
- Portability: The ORM allows the application to be more portable between different database systems (e.g., SQLite, PostgreSQL, MySQL) with minimal code changes.
- Queried leaderboard using ORM 

--- What future improvements are in store, if any? ---
The most obvious answer : implementing this with my arcade app and gathering realtime data from users rather than using faker to fill in my database! Maybe one day! :) 

Other improvements:
Enhanced Error Handling: Improve the API's error responses to provide more specific and informative messages to the client. For example, instead of a generic 400 Bad Request, the API could specify which required field is missing.

Further Performance Optimization: Add more database indexes to frequently queried columns to enhance performance. I could also explore caching mechanisms for popular API responses to reduce database load.

RESTful Design: Refine the API design by implementing more consistent resource nesting, particularly for the scores and achievements endpoints, to create a more intuitive and predictable API.

Real-time high-score updates using websockets would be cool!

______________________________________________________________________________________________________
