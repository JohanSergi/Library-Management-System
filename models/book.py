from email.policy import default

from odoo import models,fields

class book(models.Model):
    _name = 'book.records'
    _description = 'Book Records'
    _rec_name = 'title'

    book_id = fields.Integer(string="Book ID")
    title = fields.Char()
    author = fields.Char()
    price = fields.Float()
    genre = fields.Char()
    publisher = fields.Char()
    language = fields.Char()
    total_copies = fields.Integer()
    available_copies = fields.Integer()
    active = fields.Boolean(default=True)

