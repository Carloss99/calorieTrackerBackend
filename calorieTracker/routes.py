from flask import Blueprint, request, jsonify, redirect, url_for
from calorieTracker.models import db, User, FoodItem
from calorieTracker.schemas import UserSchema, FoodItemSchema
from calorieTracker import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('foods', __name__)
user_schema = UserSchema()
food_schema = FoodItemSchema()
foods_schema = FoodItemSchema(many=True)


#Register Route
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'error:"invalid'})
    username =data.get('username')
    password = data.get('password')

    if not username or not password:
        return(jsonify({"Username and password are required"}))
    if User.query.filter_by(username=username).first():
        return jsonify({"Username already exists"})
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201



#Login Route
# @bp.route('/login', methods=["POST","GET"])
# def login():
#     if request.method == "POST":
#         data = request.get_json()
#         if not data:
#             return jsonify({'error':'invalid'})

#         username = data.get('username')
#         password = data.get('password')
#         user = User.query.filter_by(username=username).first()

#         if user and bcrypt.check_password_hash(user.password, password):
#             access_token = create_access_token(identity=str(user.id))
#             print("userID" , user.id, type(user.id))
#             return jsonify(access_token=access_token)
#         return jsonify({"error": "Invalid credentials."})
#     return redirect(url_for("login"))

@bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials."}), 401


#profile route
@bp.route("/profile", methods=['GET'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "username":user.username
        })
    return jsonify({"error":"User not found"})



@bp.route("/foods", methods=["GET", "POST"])
@jwt_required()
def handle_foods():
    if request.method == "POST":
        user_id = get_jwt_identity()
        json_data = request.get_json()
    
        json_data['user_id'] = user_id
        data = food_schema.load(request.get_json())
        db.session.add(data)
        db.session.commit()
        return food_schema.jsonify(data)
    else:
        user_id = get_jwt_identity()
        entries = FoodItem.query.filter_by(user_id=user_id).all()
        return foods_schema.jsonify(entries)
    


@bp.route("/foods/<int:food_id>", methods=["PUT"])
@jwt_required()
def update_food(food_id):
    user_id = get_jwt_identity()
    food_item = FoodItem.query.filter_by(id=food_id, user_id=user_id).first()
    if not food_item:
        return jsonify({"error":"food not found"})
    data = request.get_json()

    food_item.food_name = data.get('name',food_item.name)
    food_item.calories = data.get('calories', food_item.calories)
    food_item.protien = data.get('protien',food_item.protien)
    food_item.carbs = data.get('carbs', food_item.carbs)
    food_item.fat = data.get('fat',food_item.fat)
    food_item.date = data.get('date', food_item.date)
    db.session.commit()
    return jsonify({"message": "Food updated"})
    
    

