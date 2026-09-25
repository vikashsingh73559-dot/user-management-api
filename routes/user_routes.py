from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models.user import User
from services.user_service import (
    get_users,
    get_user_by_id,
    create_user
)
import re


user_bp = Blueprint("users", __name__)


# GET /users
@user_bp.route("/users", methods=["GET"])
def get_all_users():

    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    users, total = get_users(
        search=search,
        page=page,
        limit=limit
    )

    return jsonify({
        "success": True,
        "data": [user.to_dict() for user in users],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    })


# POST /users
@user_bp.route("/users", methods=["POST"])
def create_new_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required"
        }), 400

    # Required fields
    required_fields = ["name", "email", "role"]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "error": f"{field} is required"
            }), 400

    # Email validation
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_pattern, data["email"]):
        return jsonify({
            "success": False,
            "error": "Invalid email format"
        }), 400

    # Duplicate email
    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "success": False,
            "error": "Email already exists"
        }), 409

    try:
        user = create_user(
            name=data["name"],
            email=data["email"],
            role=data["role"]
        )

    except IntegrityError:
        return jsonify({
            "success": False,
            "error": "Database error while creating user"
        }), 500

    return jsonify({
        "success": True,
        "data": user.to_dict()
    }), 201


# GET /users/<id>
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "data": user.to_dict()
    })