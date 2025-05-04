from flask import Blueprint, request, jsonify
from calorieTracker.models import db, User, FoodItem
from calorieTracker.schemas import UserSchema, FoodItemSchema
from calorieTracker import app

bp = Blueprint('api', __name__)
user_schema = UserSchema()
food_schema = FoodItemSchema()

@bp.route("/")
def home():
    return ("Nicole")

@bp.route("/foods", methods=["GET", "POST"])
def handle_foods():
    if request.method == "POST":
        data = request.get_json()
        entry = FoodItem(**data)
        return food_schema.jsonify(entry)
    else:
        entries = FoodItem.query.all()
        return food_schema.jsonify(entries)