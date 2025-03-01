"""Simple file to run oaipmh in debug mode.

Run as `python main.py`"""
import os
from oaipmh.factory import create_web_app

if __name__ == "__main__":
    os.environ['TEMPLATES_AUTO_RELOAD'] = "1"
    os.environ['DEBUG'] = "1"
    app = create_web_app()
    app.run(debug=True, port=8080)
