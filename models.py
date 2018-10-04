from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                        nullable=False,
                    )
    last_name = db.Column(db.String(50),
                        nullable=False,
                        )
    image_url = db.Column(db.Text, default='http://swaleswillis.co.uk/wp-content/uploads/2017/04/face-placeholder.gif')

    post = db.relationship('Post')

    def __repr__(self):
        return f"{self.full_name} {self.image_url}"    
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    full_name = property(get_full_name)


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                        nullable=False,
                    )
    content = db.Column(db.Text,
                        nullable=False,
                        )

    created_at = db.Column(db.DateTime,
    default=datetime.utcnow,
    nullable=False)

    user_id = db.Column(db.Integer,
    db.ForeignKey('users.id'))

    user = db.relationship('User')


