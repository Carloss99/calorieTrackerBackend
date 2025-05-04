from calorieTracker import ma
from calorieTracker.models import User, FoodItem

class FoodItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodItem

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]