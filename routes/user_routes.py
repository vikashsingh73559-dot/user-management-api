from flask import Blueprint, request, jsonify
from models.user import User, db
from sqlalchemy.exc import IntegrityError
import re


user_bp = Blueprint("users", __name__)


# GET /users
# Search: /users?search=vikash
# Pagination: /users?page=1&limit=10
@user_bp.route("/users", methods=["GET"])
def get_users():

    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    # Validate pagination
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    # Start query
    query = User.query

    # Search by name or email
    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    # Total matching users
    total = query.count()

    # Pagination
    users = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
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
def create_user():

    data = request.get_json()

    # Request body validation
    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required"
        }), 400

    # Required fields validation
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

    # Duplicate email check
    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "success": False,
            "error": "Email already exists"
        }), 409

    # Create user
    user = User(
        name=data["name"],
        email=data["email"],
        role=data["role"]
    )

    # Save to database
    try:
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

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

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "data": user.to_dict()
    })