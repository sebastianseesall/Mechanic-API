from app import create_app
from app.models import db

from flask_marshmallow import Marshmallow
from flask import Blueprint

ma = Marshmallow()

app = create_app('DevelopmentConfig')

from sqlalchemy import text

with app.app_context():
    db.create_all()
    # with db.engine.connect() as conn:
    #     conn.execute(text('ALTER TABLE service_ticket_inventory ADD COLUMN quantity INT NOT NULL DEFAULT 1;'))

if __name__ == "__main__":
    app.run()