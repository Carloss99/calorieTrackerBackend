from flask import Blueprint, request, jsonify
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
    username =data.get('username')
    password = data.get('password')

    if not username or not password:
        return(jsonify({"Username and password are required"}))
    if User.query.filter_by(username=username).first():
        return jsonify({"Username already exists"})
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201



#Login Route
@bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        print("userID" , user.id, type(user.id))
        return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid credentials."})


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
        entries = FoodItem.query.all()
        return foods_schema.jsonify(entries)