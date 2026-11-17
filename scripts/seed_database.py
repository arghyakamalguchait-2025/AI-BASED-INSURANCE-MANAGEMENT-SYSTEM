from app import create_app, seed_data
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    seed_data()
    print('Database seeded successfully.')
