from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

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
    default=datetime.now,
    nullable=False)

    def make_friendly_date(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M %p')

    friendly_date = property(make_friendly_date)

    user_id = db.Column(db.Integer,
    db.ForeignKey('users.id'))

    user = db.relationship('User')

    tags = db.relationship('Tag', secondary='posts_tags', backref = 'tags')




class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                    db.ForeignKey("posts.id"),
                    primary_key=True,
                    nullable=False
                    )
    
    tag_id  = db.Column(db.Integer, 
                    db.ForeignKey("tags.id"),
                    primary_key=True,
                    nullable=False
                )

     

    
class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    name = db.Column(db.String(50),
                        nullable=False,
                        unique=True
                    )


    posts = db.relationship('Post', secondary='posts_tags', backref = 'posts')







# post_tags = Table('PostTag', Base.metadata,
#     Column('post_id', Integer, ForeignKey('left.id'), primary_key=True),
#     Column('tag_id', Integer, ForeignKey('right.id'))
# )
