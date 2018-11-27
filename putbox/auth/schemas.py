from flask_marshmallow import Schema


class UserSchema(Schema):

    class Meta:
        # Fields to expose
        fields = ('user_id', 'username', 'email', 'register_date','user_token')


user_schema = UserSchema()
users_schema = UserSchema(many=True)