from calorieTracker import create_app, db
import click
from flask_cors import CORS

app = create_app()
CORS(app)
