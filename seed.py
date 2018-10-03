from models import User, db
from app import app

# Create all tables
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add user
Hasi = User(first_name='Hasier', last_name="Pastor")

# Add new objects to session, so they'll persist
db.session.add(Hasi)

# Commit--otherwise, this never gets saved!
db.session.commit()
