from odoo import models,fields

class user(models.Model):
    _name = 'user.records'
    _description = 'Customer Records'

    customer_id = fields.Integer(string="User ID")
    name = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    address = fields.Char()
    books_taken = fields.Integer(string="Books Due",readonly=True)

