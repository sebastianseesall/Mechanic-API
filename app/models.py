from flask import app, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import VARCHAR, Date, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from werkzeug.security import check_password_hash, generate_password_hash


customers_bp = Blueprint('customers', __name__)

# Add your route definitions here or import them

# Create a base class for our models
class Base(DeclarativeBase): 
    pass
 
#Instantiate your SQLAlchemy database

db = SQLAlchemy(model_class = Base)

#db.init_app(app) #adding our db extension to our app
#↓models objects↓
class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)

   #New relationship attribute
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('customers.id'), nullable=False)
    VIN: Mapped[str] = mapped_column(VARCHAR(17), nullable=False)
    service_description: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    service_date: Mapped[Date] = mapped_column(Date, nullable=False)

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(
        'Mechanic',
        secondary='service_mechanics',
        back_populates='service_tickets'
    )
    inventory_items: Mapped[List['Inventory']] = db.relationship(#relationship to Inventory model
        'Inventory',
        secondary='service_ticket_inventory',
        back_populates='service_tickets'
    )

class Service_mechanic(Base):
    __tablename__ = 'service_mechanics'

    ticket_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('service_tickets.id'), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('mechanics.id'), primary_key=True)

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(
        "ServiceTicket",
        secondary="service_mechanics",
        back_populates="mechanics"
    )


class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(String(255), nullable=False)
    part_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(
        'ServiceTicket',
        secondary='service_ticket_inventory', 
        back_populates='inventory_items' #use back_populates to link both sides of the relationship
    ) 

#assosication table for many-to-many relationship between ServiceTicket and Inventory
class ServiceTicketInventory(Base):
    __tablename__ = 'service_ticket_inventory'
    service_ticket_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('service_tickets.id'), primary_key=True)
    inventory_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('inventory.id'), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # <-- Additional field

    # Optional: relationships to ServiceTicket and Inventory for easier access
    service_ticket: Mapped['ServiceTicket'] = db.relationship('ServiceTicket', backref='service_ticket_inventory_items')
    inventory: Mapped['Inventory'] = db.relationship('Inventory', backref='service_ticket_inventory_items')