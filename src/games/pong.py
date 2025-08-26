"""
pong.py defines the AsciiPongGame class, which provides a text-based
version of the classic Pong game. It supports single-player gameplay
against a simple AI, maintains scores, and tracks game state.

The game can be rendered as an ASCII string suitable for console or
web-based text displays.
"""


import random

class AsciiPongGame:
    def __init__(self, width=80, height=20):
        self.width = width
        self.height = height
        self.paddle_a_y = self.height // 2
        self.paddle_b_y = self.height // 2
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])
        self.score_a = 0
        self.score_b = 0
        self.game_over = False
        self.game_started = False
        self.winner = None

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'paddle_a_y': self.paddle_a_y,
            'paddle_b_y': self.paddle_b_y,
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,

            'ball_dx': self.ball_dx,
            'ball_dy': self.ball_dy,
            'score_a': self.score_a,
            'score_b': self.score_b,
            'game_over': self.game_over,
            'game_started': self.game_started,
            'winner': self.winner
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(width=data['width'], height=data['height'])
        game.paddle_a_y = data['paddle_a_y']
        game.paddle_b_y = data['paddle_b_y']
        game.ball_x = data['ball_x']
        game.ball_y = data['ball_y']
        game.ball_dx = data['ball_dx']
        game.ball_dy = data['ball_dy']
        game.score_a = data['score_a']
        game.score_b = data['score_b']
        game.game_over = data['game_over']
        game.game_started = data['game_started']
        game.winner = data['winner']
        return game

    def render(self):
        if not self.game_started:
            return "Press 'Enter' to start the game."

        if self.game_over:
            return self._render_game_over()

        board = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(' ')
            board.append(row)

        # Draw paddles
        for y_offset in range(-2, 3):
            if 0 <= self.paddle_a_y + y_offset < self.height:
                board[self.paddle_a_y + y_offset][0] = '|'
            if 0 <= self.paddle_b_y + y_offset < self.height:
                board[self.paddle_b_y + y_offset][self.width - 1] = '|'

        # Draw ball
        if 0 <= self.ball_y < self.height and 0 <= self.ball_x < self.width:
            board[self.ball_y][self.ball_x] = 'O'

        # Draw a line in the middle
        for y in range(self.height):
            board[y][self.width // 2] = '·'

        rendered_board = ""
        for row in board:
            rendered_board += "".join(row) + "\n"

        score_board = f"SCORE: PLAYER A: {self.score_a} | PLAYER B: {self.score_b}\n\n"
        return score_board + rendered_board

    def update(self):
        if self.game_over:
            return

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        self._check_collisions()
        self._update_computer_paddle()
        self._check_for_win()

    def _check_collisions(self):
        # Top and bottom wall collisions
        if self.ball_y <= 0 or self.ball_y >= self.height - 1:
            self.ball_dy *= -1

        # Paddle A collision
        if self.ball_x <= 1 and self.paddle_a_y - 2 <= self.ball_y <= self.paddle_a_y + 2:
            self.ball_dx *= -1

        # Paddle B (computer) collision
        if self.ball_x >= self.width - 2 and self.paddle_b_y - 2 <= self.ball_y <= self.paddle_b_y + 2:
            self.ball_dx *= -1

        # Check for scoring
        if self.ball_x < 0:
            self.score_b += 1
            self._reset_ball()
        elif self.ball_x >= self.width:
            self.score_a += 1
            self._reset_ball()

    def _update_computer_paddle(self):
        # Simple AI to follow the ball
        if self.ball_y > self.paddle_b_y:
            self.paddle_b_y += 1
        elif self.ball_y < self.paddle_b_y:
            self.paddle_b_y -= 1

        # Keep the paddle within bounds
        if self.paddle_b_y < 2:
            self.paddle_b_y = 2
        elif self.paddle_b_y > self.height - 3:
            self.paddle_b_y = self.height - 3

    def _reset_ball(self):
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])

    def change_paddle_direction(self, paddle_name, direction):
        if paddle_name == 'A':
            self.paddle_a_y += direction
            # Keep paddle A within bounds
            if self.paddle_a_y < 2:
                self.paddle_a_y = 2
            elif self.paddle_a_y > self.height - 3:
                self.paddle_a_y = self.height - 3

    def _check_for_win(self):
        if self.score_a >= 5:
            self.winner = 'Player A'
            self.game_over = True
        elif self.score_b >= 5:
            self.winner = 'Player B'
            self.game_over = True

    def _render_game_over(self):
        message = f"GAME OVER! {self.winner} WINS!\n"
        score_display = f"Final Score: Player A {self.score_a} - Player B {self.score_b}\n"
        instructions = "Press 'R' to reset or 'Back to Menu' to return to the main screen."
        return message + score_display + instructions

    def reset(self):
        self.__init__(self.width, self.height)

