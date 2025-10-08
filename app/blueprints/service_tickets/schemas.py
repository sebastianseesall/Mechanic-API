from marshmallow import Schema, fields

class ServiceTicketSchema(Schema):
    customer_id = fields.Integer(required=True)
    VIN = fields.String(required=True)
    service_description = fields.String(required=True)
    service_date = fields.Date(required=True)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)