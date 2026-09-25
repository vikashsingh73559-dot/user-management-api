from models.user import User, db


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def search_users(search_term):
    return User.query.filter(
        db.or_(
            User.name.ilike(f"%{search_term}%"),
            User.email.ilike(f"%{search_term}%")
        )
    ).all()


def create_user(name, email, role):
    user = User(
        name=name,
        email=email,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return user