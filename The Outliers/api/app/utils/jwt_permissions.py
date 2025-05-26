from datetime import timedelta

from flask_jwt_extended import create_access_token

from app.models import User


def get_user_from_jwt(jwt):
	return User.query.get(jwt.get('sub'))


def build_token(user: User):
	access_token = create_access_token(
		identity=str(user.id),
		expires_delta=timedelta(hours=1)
	)

	return access_token


def validate_permissions(jwt):
	user = get_user_from_jwt(jwt)

	if not user:
		return False

	return True
