"""
arcade_game.py defines the handling for arcade game interactions through requests from the frontend.
It supports multiple ASCII-base games including Snake, Pong and Tic Tac Toe.
"""

import json
from flask import Blueprint, jsonify, request, session, abort
from sqlalchemy import desc
from ..games.snake import AsciiSnakeGame
from ..games.pong import AsciiPongGame
from ..games.tic_tac_toe import TicTacToeGame

# Session key to store game instances
SESSION_GAMES_KEY = 'current_games'

bp = Blueprint('arcade_game', __name__, url_prefix='/arcade')

def get_game_instance(game_name):
    """
    Retrieve or initialize a game instance from the session.
    """
    games_data = session.get(SESSION_GAMES_KEY, {})
    game_data = games_data.get(game_name)
    game = None

    if game_name == 'snake_ascii':
        game = AsciiSnakeGame.from_dict(game_data) if game_data else AsciiSnakeGame()
    elif game_name == 'pong_ascii':
        game = AsciiPongGame.from_dict(game_data) if game_data else AsciiPongGame()
    elif game_name == 'tic_tac_toe':
        game = TicTacToeGame.from_dict(game_data) if game_data else TicTacToeGame()

    if game:
        games_data[game_name] = game.to_dict()
        session[SESSION_GAMES_KEY] = games_data

    return game, games_data


# The get_top_high_score function and the high_scores and save_high_score
# endpoints have been removed as they are no longer needed without the
# HighScore model.


@bp.route('/play', methods=['POST'])
def play_game():
    """
    Main endpoint to handle game actions from the frontend.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    game_name = data.get('game_name')
    user_input = data.get('input', '').strip()
    snake_direction = data.get('snake_direction')
    paddle_a_move_direction = data.get('paddle_a_move_direction')

    game, games_data = get_game_instance(game_name)

    if not game:
        return jsonify({
            'output': 'Error: Game not found or not initialized in session.',
            'state': 'error'
        }), 400

    game_state_for_frontend = 'playing'
    output = ""
    extra_response_data = {}

    if user_input.lower() == 'start':
        game.reset()
        if hasattr(game, 'game_started'):
            game.game_started = True

        if game_name == 'tic_tac_toe':
            output = game.render()
        elif game_name == 'snake_ascii':
            # The game render now no longer takes a high_score_data argument.
            output = game.render()
        else:
            output = game.render()

        if game_name == 'tic_tac_toe':
            extra_response_data.update({
                'human_player': game.human_player,
                'ai_player': game.ai_player,
                'current_player': game.current_player,
                'game_internal_state': game.state
            })
            game_state_for_frontend = game.state
        elif hasattr(game, 'game_over'):
            game_state_for_frontend = 'game_over' if game.game_over else 'playing'
            if game.game_over and hasattr(game, 'score') and game_name == 'snake_ascii':
                extra_response_data['score'] = game.score

    elif game_name == 'pong_ascii' and user_input.lower() == 'update':
        if not game.game_over:
            if paddle_a_move_direction is not None:
                game.change_paddle_direction('A', paddle_a_move_direction)
            game.update()
        output = game.render()
        game_state_for_frontend = 'game_over' if game.game_over else 'playing'

    elif game_name == 'snake_ascii' and user_input.lower() == 'update':
        if not game.game_over:
            if snake_direction:
                game.change_direction(snake_direction)
            game.update()
        # The game render now no longer takes a high_score_data argument.
        output = game.render()
        game_state_for_frontend = 'game_over' if game.game_over else 'playing'
        if game.game_over and hasattr(game, 'score'):
            extra_response_data['score'] = game.score
            # Logic to save the high score has been removed.

    else:
        if hasattr(game, 'play'):
            output = game.play(user_input)

            if game_name == 'tic_tac_toe':
                extra_response_data.update({
                    'human_player': game.human_player,
                    'ai_player': game.ai_player,
                    'current_player': game.current_player,
                    'game_internal_state': game.state
                })
                game_state_for_frontend = game.state
            elif hasattr(game, 'game_over'):
                game_state_for_frontend = 'game_over' if game.game_over else 'playing'
                if game.game_over and hasattr(game, 'score') and game_name == 'snake_ascii':
                    extra_response_data['score'] = game.score
                    # Logic to save the high score has been removed.
        else:
            output = "Invalid command for this game."
            game_state_for_frontend = 'error'

    # Save updated game state to session
    if hasattr(game, 'to_dict'):
        games_data[game_name] = game.to_dict()
        session[SESSION_GAMES_KEY] = games_data

    response_data = {
        'output': output,
        'state': game_state_for_frontend,
        **extra_response_data
    }

    return jsonify(response_data)
