from models.user import User, db


def get_users(search="", page=1, limit=10):
    query = User.query

    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    total = query.count()

    users = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return users, total


def get_user_by_id(user_id):
    return User.query.get(user_id)


def create_user(name, email, role):
    user = User(
        name=name,
        email=email,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return user