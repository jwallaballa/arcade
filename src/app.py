"""
src/app.py

This is the flask application entry point. Uses the factory function to
create the app.
"""

from . import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)